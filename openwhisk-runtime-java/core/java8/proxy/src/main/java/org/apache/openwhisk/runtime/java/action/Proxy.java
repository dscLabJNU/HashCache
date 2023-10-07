/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.openwhisk.runtime.java.action;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.lang.Process;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.concurrent.CountDownLatch;
import java.util.stream.Collectors;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import okhttp3.*;

public class Proxy {
    private HttpServer server;

    private JarLoader loader = null;
    private String proxyAddrProduce = "hashcache-global-proxy.default"; // For k8s production env
    private String proxyAddrLocal = "172.17.0.1"; // interface docker0's ip, for docker local dev env
    private String socks5Port = "8673";
    private String httpPort = "8674";
    private OkHttpClient client = new OkHttpClient();

    private String getProxyAddr() {
        String OWDEV_APIGATEWAY_PORT = System.getenv().getOrDefault("OWDEV_APIGATEWAY_PORT", "None");
        if (OWDEV_APIGATEWAY_PORT.equals("None")) {
            System.out.println("====You are in local dev environment====");
            // In local dev env
            return proxyAddrLocal;
        } else {
            // In k8s env
            System.out.println("====You are in k8s production environment====");
            return proxyAddrProduce;
        }
    }

    public Proxy(int port) throws IOException {
        this.server = HttpServer.create(new InetSocketAddress(port), -1);

        this.server.createContext("/init", new InitHandler());
        this.server.createContext("/run", new RunHandler());
        this.server.setExecutor(null); // creates a default executor
    }

    public void start() {
        String proxyAddr = getProxyAddr();
        System.setProperty("http.proxyHost", proxyAddr);
        System.setProperty("http.proxyPort", httpPort);

        System.setProperty("https.proxyHost", proxyAddr);
        System.setProperty("https.proxyPort", httpPort);

        System.setProperty("socksProxyHost", proxyAddr);
        System.setProperty("socksProxyPort", socks5Port);
        server.start();
    }

    private static void writeResponse(HttpExchange t, int code, String content) throws IOException {
        byte[] bytes = content.getBytes(StandardCharsets.UTF_8);
        t.sendResponseHeaders(code, bytes.length);
        OutputStream os = t.getResponseBody();
        os.write(bytes);
        os.close();
    }

    private static void writeError(HttpExchange t, String errorMessage) throws IOException {
        JsonObject message = new JsonObject();
        message.addProperty("error", errorMessage);
        writeResponse(t, 502, message.toString());
    }

    private static void writeLogMarkers() {
        System.out.println("XXX_THE_END_OF_A_WHISK_ACTIVATION_XXX");
        System.err.println("XXX_THE_END_OF_A_WHISK_ACTIVATION_XXX");
        System.out.flush();
        System.err.flush();
    }

    private class InitHandler implements HttpHandler {
        public void handle(HttpExchange t) throws IOException {
            if (loader != null) {
                String errorMessage = "Cannot initialize the action more than once.";
                System.err.println(errorMessage);
                Proxy.writeError(t, errorMessage);
                return;
            }

            try {
                InputStream is = t.getRequestBody();
                JsonParser parser = new JsonParser();
                JsonElement ie = parser.parse(new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8)));
                JsonObject inputObject = ie.getAsJsonObject();

                if (inputObject.has("value")) {
                    JsonObject message = inputObject.getAsJsonObject("value");
                    if (message.has("main") && message.has("code")) {
                        String mainClass = message.getAsJsonPrimitive("main").getAsString();
                        String base64Jar = message.getAsJsonPrimitive("code").getAsString();

                        // FIXME: this is obviously not very useful. The idea is that we
                        // will implement/use a streaming parser for the incoming JSON object so that we
                        // can stream the contents of the jar straight to a file.
                        InputStream jarIs = new ByteArrayInputStream(base64Jar.getBytes(StandardCharsets.UTF_8));

                        // Save the bytes to a file.
                        Path jarPath = JarLoader.saveBase64EncodedFile(jarIs);

                        // Start up the custom classloader. This also checks that the
                        // main method exists.
                        loader = new JarLoader(jarPath, mainClass);

                        Proxy.writeResponse(t, 200, "OK");
                        return;
                    }
                }

                Proxy.writeError(t, "Missing main/no code to execute.");
                return;
            } catch (Exception e) {
                e.printStackTrace(System.err);
                writeLogMarkers();
                Proxy.writeError(t, "An error has occurred (see logs for details): " + e);
                return;
            }
        }
    }

    private class RunHandler implements HttpHandler {
        public void handle(HttpExchange t) throws IOException {
            if (loader == null) {
                Proxy.writeError(t, "Cannot invoke an uninitialized action.");
                return;
            }

            ClassLoader cl = Thread.currentThread().getContextClassLoader();
            SecurityManager sm = System.getSecurityManager();

            try {
                InputStream is = t.getRequestBody();
                JsonParser parser = new JsonParser();
                JsonObject body = parser.parse(new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8))).getAsJsonObject();
                JsonParser json = new JsonParser();
                JsonObject payloadForJsonObject = json.parse("{}").getAsJsonObject();
                JsonArray payloadForJsonArray = json.parse("[]").getAsJsonArray();
                Boolean isJsonObjectParam = true;
                JsonElement inputJsonElement = body.get("value");
                if (inputJsonElement.isJsonObject()) {
                    payloadForJsonObject = inputJsonElement.getAsJsonObject();
                } else {
                    payloadForJsonArray = inputJsonElement.getAsJsonArray();
                    isJsonObjectParam = false;
                }

                HashMap<String, String> env = new HashMap<String, String>();
                Set<Map.Entry<String, JsonElement>> entrySet = body.entrySet();
                for (Map.Entry<String, JsonElement> entry : entrySet) {
                    try {
                        if (!entry.getKey().equalsIgnoreCase("value"))
                            env.put(String.format("__OW_%s", entry.getKey().toUpperCase()), entry.getValue().getAsString());
                    } catch (Exception e) {
                    }
                }

                Thread.currentThread().setContextClassLoader(loader);
                System.setSecurityManager(new WhiskSecurityManager());

                Method mainMethod = null;
                String mainMethodName = loader.entrypointMethodName;
                if (isJsonObjectParam) {
                    mainMethod = loader.mainClass.getMethod(mainMethodName, new Class[]{JsonObject.class});
                } else {
                    mainMethod = loader.mainClass.getMethod(mainMethodName, new Class[]{JsonArray.class});
                }
                mainMethod.setAccessible(true);
                int modifiers = mainMethod.getModifiers();
                if ((mainMethod.getReturnType() != JsonObject.class && mainMethod.getReturnType() != JsonArray.class) || !Modifier.isStatic(modifiers) || !Modifier.isPublic(modifiers)) {
                    throw new NoSuchMethodException(mainMethodName);
                }

                // 发送询问proxy的异步请求
                String actionName;
                if (body.has("action_name")) actionName = body.get("action_name").getAsString();
                else actionName = "Unknown";
                System.out.println("actionName: "+actionName);
                Call asyncCallForNotifyActionName = notifyActionName(actionName);
                String shouldBeDefaultValue = receiveQueryProxyAsyncRequest(asyncCallForNotifyActionName);
                if(shouldBeDefaultValue.equals("defaultValue"))
                    System.out.println("The runtime has already notified proxy of the actionName");
                
                // User code starts running here. the return object supports JsonObject and JsonArray both.                
                Object output;
                Call asyncCallForQueryIOType = sendQueryProxyAsyncRequest(actionName);
                if (isJsonObjectParam) {
                    loader.augmentEnv(env);
                    output = mainMethod.invoke(null, payloadForJsonObject);
                } else {
                    loader.augmentEnv(env);
                    output = mainMethod.invoke(null, payloadForJsonArray);
                }
//                System.out.println("output: "+ output+" type: "+output.getClass().toString());
                JsonObject jsonOutput = (JsonObject) output;
                Boolean isIOAccess = analyzeQueryRequest(asyncCallForQueryIOType);
                System.out.println("Is IO Access? " + isIOAccess);
                // This will apply into the original ${output} automatically
                jsonOutput.addProperty("is_open", isIOAccess);
                // User code finished running here.

                if (output == null) {
                    throw new NullPointerException("The action returned null");
                }

                Proxy.writeResponse(t, 200, output.toString());
                return;
            } catch (InvocationTargetException ite) {
                // These are exceptions from the action, wrapped in ite because
                // of reflection
                Throwable underlying = ite.getCause();
                underlying.printStackTrace(System.err);
                Proxy.writeError(t,
                        "An error has occurred while invoking the action (see logs for details): " + underlying);
            } catch (Exception e) {
                e.printStackTrace(System.err);
                Proxy.writeError(t, "An error has occurred (see logs for details): " + e);
            } finally {
                writeLogMarkers();
                System.setSecurityManager(sm);
                Thread.currentThread().setContextClassLoader(cl);
            }
        }

        private Call sendQueryProxyAsyncRequest(String actionName) {
            // proxyAddr: hashcache-global-proxy.default
            Request request = new Request.Builder()
                    .url("http://" + getProxyAddr() + "/queryIOType?actionName=" + actionName)
                    .get()
                    .build();
            return client.newCall(request);
        }

        private Call notifyActionName(String actionName) {
            // proxyAddr: hashcache-global-proxy.default
            Request request = new Request.Builder()
                    .url("http://" + getProxyAddr() + "/notifyActionName?actionName=" + actionName)
                    .get()
                    .build();
            return client.newCall(request);
        }
    }

    private Boolean analyzeQueryRequest(Call asyncCall) {
        String jsonRes = receiveQueryProxyAsyncRequest(asyncCall);
        System.out.println("MY jsonRes is: " + jsonRes);
        if (jsonRes.equals("R")) return false;

        /**
         * Other, jsonRes may be 'W' or 'NotWriteYet', or DefaultValue
         * We assume it happens IO operation for the uncertain situations
         */
        return true;
    }

    private String receiveQueryProxyAsyncRequest(Call asyncCall) {
        final Map<String, String> resultMap = new HashMap<>();
        // Wait for the response
        CountDownLatch countDownLatch = new CountDownLatch(1);
        asyncCall.enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                System.out.println("Async call is failure because");
                e.printStackTrace();
                countDownLatch.countDown();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                String jsonRes = response.body().string();
                System.out.println("Async call is success!! jsonRes: " + jsonRes);
                resultMap.put("json", jsonRes);
                countDownLatch.countDown();
            }
        });
        try {
            countDownLatch.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return resultMap.getOrDefault("json", "DefaultValue");
    }

    public static Boolean analyzeSocketPorts(String filePath) throws IOException {
        List<String> list = Files.readAllLines(Paths.get(filePath));
        // Socket connections shown after the second line.
        list.remove(0);
        Set<Integer> portSet = new HashSet<>();
        // list.forEach(line -> System.out.println(line + "-> port: " + Integer.parseInt(line.substring(29, 33), 16)));
        list.forEach(line -> portSet.add((Integer.parseInt(line.substring(29, 33), 16))));
        System.out.println("ports: " + portSet);
        // Every container opens 0000 port for local socket communication
        portSet.remove(Integer.valueOf("0000"));
        // This 8080 ports is for communication with OpenWhisk
        portSet.remove(Integer.valueOf("8080"));
        // I/O proxy port
        portSet.remove(Integer.valueOf("8673"));
        System.out.println("Unique port list: " + portSet);
        // Openwhisk invoker creates another connection with this proxy for sending invocation
        if (1 == portSet.size())
            return false;
        else return true;
    }

    @Deprecated
    private static void copyTCPFile(String sourcePath, String destPath, HttpExchange t) throws IOException {
        try {
            String copyCmd = "cp " + sourcePath + " " + destPath;
            System.out.println("copyCmd: " + copyCmd);
            Process process = Runtime.getRuntime().exec(copyCmd);
            int status = process.waitFor();
            if (status != 0) {
                System.err.println("Failed to copy file and the return status's is: " + status);
            }
        } catch (Exception e) {
            e.printStackTrace();
            Proxy.writeError(t, "An error has occurred (see logs for details): " + e);
        }
    }

    /**
     * Compares the difference of two files and prints it
     *
     * @param oldFile old file
     * @param newFile new file
     * @throws IOException exception
     */
    @Deprecated
    public static List<Integer> compareTwoFile(String oldFile, String newFile) throws IOException {
        List<String> list1 = Files.readAllLines(Paths.get(oldFile));
        List<String> list2 = Files.readAllLines(Paths.get(newFile));

        List<Integer> ports = new ArrayList<>();
        System.out.printf("Comparing %s and %s\n", oldFile, newFile);
        List<String> finalList = list2.stream().filter(line ->
                list1.stream().filter(line2 -> line2.equals(line)).count() == 0
        ).collect(Collectors.toList());
        if (finalList.size() == 0) {
            System.out.println("They are the same");
        } else {
//            System.out.println("Recording the ports: ");
//            finalList.forEach(one -> ports.add(Integer.parseInt(one.substring(29, 33), 16)));
            System.out.println("Here is the difference: ");
            finalList.forEach(System.out::println);

        }
        return ports;
    }


    public static void main(String args[]) throws Exception {
        Proxy proxy = new Proxy(8080);
        proxy.start();
    }
}

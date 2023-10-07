package org.apache.openwhisk.core.containerpool.Plugin

import org.apache.openwhisk.common.Logging
import org.apache.openwhisk.core.entity.{ActivationId, ActivationResponse, WhiskActivation}
import spray.json.JsObject

import scala.collection.mutable
import scala.concurrent.Future

object HashCache {
  // Caches the data after executing more than this value
  val cacheThreshold: Int = scala.util.Properties.envOrElse("cacheThreshold", "3").toInt
  // The number of executions of each action
  var numExecutionsAction: mutable.Map[String, mutable.Map[Int, Int]] =
    mutable.Map[String, mutable.Map[Int, Int]]().withDefault(k => mutable.Map())

  // Apply the HashCache by caching the result after the action completed
  val enableCacheString: String = scala.util.Properties.envOrElse("enableHashCache", "false")
  val enableCache: Boolean = if (enableCacheString.equals("true")) true else false
  var actionRelationship: mutable.Map[String, mutable.Map[Int, Set[ActivationResponse]]] =
    mutable.Map[String, mutable.Map[Int, Set[ActivationResponse]]]().withDefault(d => mutable.Map().withDefault(_ => Set()))

  // Apply the HashCache by caching postedFuture
  val enableCachePostedFutureString: String = scala.util.Properties.envOrElse("enableCachePostedFuture", "true")
  val enableCachePostedFuture: Boolean = if (enableCachePostedFutureString.equals("true")) true else false
  var actionRelationShipPostedFuture: mutable.Map[String, mutable.Map[Int, Set[Future[Future[Either[ActivationId, WhiskActivation]]]]]] =
    mutable.Map[String, mutable.Map[Int, Set[Future[Future[Either[ActivationId, WhiskActivation]]]]]]().withDefault(_ => mutable.Map().withDefault(_ => Set()))

  def getHashCode(str: JsObject): Int = {
    util.hashing.MurmurHash3.stringHash(str.toString())
  }

  def matchCacheConditions(actionName: String, actionPramsCode: Int)(implicit logging: Logging): Boolean = {
    if (enableCache) {
      val actionExecuted = actionRelationship.contains(actionName) && actionRelationship(actionName).contains(actionPramsCode)
      val onlyOneResult = actionRelationship(actionName)(actionPramsCode).size == 1
      val numExecActionSatisfied = {
        numExecutionsAction.contains(actionName) && // action has been exeucted
          numExecutionsAction(actionName).contains(actionPramsCode) && // action with specific params has been executed
          numExecutionsAction(actionName)(actionPramsCode) >= cacheThreshold // the number of execution of action has enough
      }
      val isMatched = actionExecuted && onlyOneResult && numExecActionSatisfied && enableCache
      if (isMatched)
        logging.info(this, s"[matchCacheConditions]: actionName: $actionName, actionRelationship: ${actionRelationship}")
      isMatched
    }
    else false
  }

  def cacheAction(actionName: String, actionPramsCode: Int, newResponse: ActivationResponse)(implicit logging: Logging): Unit = {
    val numExecAction = {
      if (numExecutionsAction.contains(actionName)) {
        numExecutionsAction(actionName)(actionPramsCode) += 1
      }
      else {
        numExecutionsAction(actionName) = mutable.Map(actionPramsCode -> 1).withDefault(k => 0)
      }
      numExecutionsAction(actionName)(actionPramsCode)
    }
    logging.info(this, s"numExecutionsAction is :${numExecutionsAction}")

    logging.info(this, s"number of [$actionName($actionPramsCode)] invocation is: ${numExecAction}")

    // Caches the output data of the action
    // if (numExecAction >= cacheThreshold){
    if (actionRelationship.contains(actionName)) {
      actionRelationship(actionName)(actionPramsCode) += newResponse
    }
    else {
      actionRelationship(actionName) = mutable.Map(actionPramsCode -> Set(newResponse)).withDefault(k => Set())
    }

    logging.info(this, s"Cached: [action: $actionPramsCode], result: ${actionRelationship(actionName)(actionPramsCode)} ]")
  }

  def matchCacheConditionsPostedFuture(actionName: String, actionPramsCode: Int)(implicit logging: Logging): Boolean = {
    if (enableCachePostedFuture) {
      var onlyOneResult = false
      var IOAccess = false
      val postedFutureMap = actionRelationShipPostedFuture
      val numExecAction = numExecutionsAction

      val numExecActionSatisfied = {
        numExecAction.contains(actionName) && // action has been exeucted
          numExecAction(actionName).contains(actionPramsCode) && // action with specific params has been executed
          numExecAction(actionName)(actionPramsCode) >= cacheThreshold // the number of execution of action has enough
      }

      if (numExecActionSatisfied) {
        val activationResponseSet = postedFutureMap(actionName)(actionPramsCode) map {
          // Iterates all cached responses, marking they to cacheable when the conditions are met.
          postedFuture =>
            // I know this is unappetizing...
            postedFuture.value.get.get.value.get.get match {
              case Right(value) =>
                val response = value.response
                if (response.hasIOAccess.getOrElse(true)) {
                  // Filter out functions that determine no IO behavior by setting IOAceess=false
                  IOAccess = true
                }
                response
              case _ => // It will never happend in blocking invocation
            }
        }
        onlyOneResult = if (activationResponseSet.size == 1) true else false
      }

      val isMatched = numExecActionSatisfied && onlyOneResult && !IOAccess
      if (isMatched)
        logging.info(this, s"[matchCacheConditionsPostedFuture]: actionName: $actionName, postedFutureMap: ${postedFutureMap}")
      isMatched
    }
    else false
  }

  def cacheWhiskPostedFuture(actionName: String, actionPramsCode: Int, postedFuture: Future[Future[Either[ActivationId, WhiskActivation]]])(implicit logging: Logging): Unit = {
    if (enableCachePostedFuture) {
      if (numExecutionsAction.contains(actionName)) {
        numExecutionsAction(actionName)(actionPramsCode) += 1
      }
      else {
        numExecutionsAction(actionName) = mutable.Map(actionPramsCode -> 1).withDefault(k => 0)
      }
      numExecutionsAction(actionName)(actionPramsCode)


      if (actionRelationShipPostedFuture.contains(actionName)) {
        actionRelationShipPostedFuture(actionName)(actionPramsCode) += postedFuture
      }
      else {
        actionRelationShipPostedFuture(actionName) = mutable.Map(actionPramsCode -> Set(postedFuture)).withDefault(k => Set())
      }

      logging.info(this, s"Cached: [action: $actionPramsCode], result: ${
        actionRelationShipPostedFuture(actionName)(actionPramsCode)
      } ]")
    }
  }
}

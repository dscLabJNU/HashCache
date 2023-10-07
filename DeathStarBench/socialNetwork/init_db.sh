docker-compose up -d
# docker-compose -f docker-compose-sharding.yml up -d


pip3 install -r requirements.txt

# Small dataset
python3 scripts/init_social_graph.py --graph=socfb-Reed98
# # Medium dataset
# python3 scripts/init_social_graph.py --graph=ego-twitter
# # Large dateset
# python3 scripts/init_social_graph.py --graph=soc-twitter-follows-mun
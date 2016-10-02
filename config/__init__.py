import yaml
import os
import logging
import sys

logger = logging.getLogger(__name__)

config = {}

path = '../conf.yml'

mode = os.environ.get('WORLDMAP_MODE') or 'develop'

if os.path.isfile(path):
    with open(path) as conf:
        logger.error('using conf in %s' % path)
        c = yaml.load(conf)
    default_conf = c.get('default')
    specific_conf = c.get(mode, {})
    if not specific_conf:
        logger.error('config for %s not found' % mode)
    config = {**default_conf, **specific_conf}
    if not config:
        logger.error('no config found in path %s!' % (os.path.abspath(path)))
    print(config)

else:
    logger.error('no config found in path %s!' % (os.path.abspath(path)))




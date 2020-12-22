import logging
logger = logging.getLogger(__name__)

def add_loglevel(level, levelName):
    logging.addLevelName(level, levelName)
    def func(self, message, *args, **kws):
        if self.isEnabledFor(level):
            # Yes, logger takes its '*args' as 'args'.
            self._log(level, message, args, **kws) 

    setattr(logging.Logger, levelName.lower(), func)

def set_loglevel(verbose=0):
    if verbose > 3:
        loglevel = logging.DEBUG
    elif verbose > 2:
        loglevel = logging.INFO
    elif verbose > 1:
        loglevel = logging.WARNING
    elif verbose > 0:
        loglevel = logging.ERROR
    else:
        loglevel = logging.CRITICAL
    
    logging.basicConfig(level=loglevel,
            format='%(asctime)s [%(levelname)s] %(message)s')
    
    logger.info("set log level %s" % logging.getLevelName(loglevel))

add_loglevel(logging.CRITICAL - 1 , "NOTICE")
add_loglevel(logging.CRITICAL - 2, "TEST")

debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
exception = logger.exception
fatal = logger.fatal
notice = logger.notice
test = logger.test



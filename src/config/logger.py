import os
import logging
import logging.handlers


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self):
        self.logger_home = os.environ.get('LOG_PATH')
        if self.logger_home is None:
            project_home = os.environ.get('PROJECT_HOME')
            if project_home is None:
                self.logger_home = 'logs'
            else:
                self.logger_home = os.path.join(project_home, 'logs')

        if not os.path.exists(self.logger_home):
            os.makedirs(self.logger_home)

        self.app_logger = self.app_logger()

    def app_logger(self):
        app_logger = logging.getLogger('app_logger')
        app_logger.propagate = False
        format_str = logging.Formatter('%(asctime)s`%(message)s')
        app_logger.setLevel(logging.INFO)
        senv = os.environ.get("SERVER_ENV")
        if senv is None:
            sh = logging.StreamHandler()
            sh.setFormatter(format_str)
            app_logger.addHandler(sh)

        th = logging.handlers.TimedRotatingFileHandler(filename=os.path.join(self.logger_home, 'app.log'),
                                                       when='MIDNIGHT', encoding='utf-8', backupCount=30)
        th.setFormatter(format_str)
        app_logger.addHandler(th)
        return app_logger


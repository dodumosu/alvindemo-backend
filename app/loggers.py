# -*- coding: utf-8 -*-
import datetime

from pythonjsonlogger import jsonlogger

APP_NAME = "DemoAPI"


def add_app_name(logger, log_method, event_dict):
    event_dict["application"] = APP_NAME

    return event_dict


class JsonLogFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        for field in self._required_fields:
            log_record[field] = record.__dict__.get(field)
        log_record.update(message_dict)

        if "timestamp" not in log_record:
            now = datetime.datetime.now(tz=datetime.timezone.utc)
            log_record["timestamp"] = datetime.datetime.strftime(
                now, format="%Y-%m-%dT%H:%M:%S.%f%z"
            )

        if "application" not in log_record:
            log_record["application"] = APP_NAME

        jsonlogger.merge_record_extra(
            record, log_record, reserved=self._skip_fields
        )

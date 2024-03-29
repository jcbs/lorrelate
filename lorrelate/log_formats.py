import os, sys, re, collections
import datetime as dt
from tabulate import tabulate


class LogEntry:

    def __init__(self, timestamp, message):
        """
        Log Entry

        Parameters
        ----------
        timestamp: type datetime.datetime
            timestamp of log event
        message: type str
            log message
        """
        self.timestamp = timestamp
        self.message = message

    def __str__(self):
        return f"{self.timestamp} -- {self.message}"

    def __repr__(self):
        return f"{self.timestamp} -- {self.message}"

class LogFile:

    def __init__(self, path, log_format=None, timestamp_format=None):
        self.path = path
        self.log_format = log_format
        self.timestamp_format = timestamp_format

        with open(path) as f:
            # self.raw_log_data = f.read()
            self.log_data = [line.strip() for line in f]

    def __str__(self):
        return f"{self.path}"

    def __repr__(self):
        return f"{self.path}"

    def get_entries(self, to_timestamp=True, as_dict=True):
        if as_dict:
            entries = {}
        else:
            entries = []

        for line in self.log_data:
            date = find_time_stamp(line, timestamp_format=self.timestamp_format)

            if to_timestamp:
                tmp_timestamp_fmt = self.timestamp_format

                if not '%Y' in tmp_timestamp_fmt:
                    tmp_timestamp_fmt = '%Y ' + tmp_timestamp_fmt
                    full_date = str(dt.datetime.today().year) + ' ' + date
                else:
                    full_date = date

                full_date = dt.datetime.strptime(full_date, tmp_timestamp_fmt)

            if as_dict:
                full_date = str(full_date)
                entries[full_date] = line.split(date)[-1]
            else:
                entry = LogEntry(timestamp=full_date, message=line.split(str(date))[-1])
                entries.append(entry)
        self.entries = entries


unit_dict = {
            'w': 'weeks',
            'd': 'days',
            'h': 'hours',
            'min': 'minutes',
            's': 'seconds',
            'ms': 'milliseconds',
            'us': 'microseconds',
        }


def in_datetime_range(test_time, base_time, before=0, after=0):
    if isinstance(before, int) or isinstance(before, float):
        before = {'seconds': before}
    elif isinstance(before, str) and ' ' in before:
        value, unit = before.split(' ')
        before = {unit_dict[unit]: float(value)}

    if isinstance(after, int) or isinstance(after, float):
        after = {'seconds': after}
    elif isinstance(after, str) and ' ' in after:
        value, unit = after.split(' ')
        after = {unit_dict[unit]: float(value)}

    delta_t_before = dt.timedelta(**before)
    delta_t_after = dt.timedelta(**after)

    start = base_time - delta_t_before
    end = base_time + delta_t_after
    return (test_time == base_time) or ((test_time >= start) and (test_time <= end))


def match_events(primary_log_file, secondary_log_file,
        primary_contents=None, secondary_contents=None,
        before=0, after=0,
        ):
    matches = {}
    primary_log_file.get_entries(as_dict=False)
    entries1 = primary_log_file.entries
    secondary_log_file.get_entries(as_dict=False)
    entries2 = secondary_log_file.entries

    for e1 in entries1:
        t1 = e1.timestamp
        in_dict = False
        for e2 in entries2:
            t2 = e2.timestamp
            if in_datetime_range(t2, t1, before, after): #e1.timestamp == e2.timestamp:
                if (relevant_event(str(e1.message), primary_contents)
                        and relevant_event(str(e2.message), secondary_contents)
                    ):
                    if not in_dict:
                        matches[str(e1.timestamp)] = [e1.message]
                        in_dict = True
                    matches[str(e1.timestamp)].append(e2.message)
    return matches


def relevant_event(test_string, content):
    if content:
        return (content in test_string)
    else:
        return True


def find_time_stamp(string, timestamp_format):
    """
    Find timestamp according to format in string.

    Parameters
    ----------
    string: type str
        string to search for timestamp
    timestamp_format: type regex

    """
    formats = re.findall(r"%\w", timestamp_format)
    date_string = timestamp_format

    for s in formats:
        r = string_dict()[s]
        date_string = re.sub(s, r, date_string)

    date_string = re.search(date_string, string)

    return date_string.group()


def string_dict():
    """
    Returns dictionary, which translates format to regex.
    """
    str_dict = {
            #'%D': '[ 0-9][0-9]',
            '%d': '[ 0-9][0-9]',
            #'%d': '\\\\d{2}',
            '%m': '\\\\d{2}',
            '%b': '\\\\w{3}',
            '%Y': '\\\\d{4}',
            '%H': '\\\\d{2}',
            '%M': '\\\\d{2}',
            '%S': '\\\\d{2}',
            }
    return str_dict


#timestamp = dt.datetime.strptime(date_string, date_format)

if __name__ == "__main__":
    test = 'Jun 24 18:22:01'
    test1 = test + "hello world"
    test2 = "2021 " + test
    test3 = "hallo datum " + test2 + " das ist ja spannend"
    fmt = '%Y %b %d %H:%M:%S'
    fmt1 = '%b %d %H:%M:%S'
    fmt2 = '%b %d %H:%M:%S'
    fmt3 = '%Y-%m-%d %H:%M:%S'

    match = find_time_stamp(test3, fmt)
    match1 = find_time_stamp(test1, fmt1)

    log1 = LogFile("/var/log/kern.log.1", timestamp_format=fmt2)
    #log1 = LogFile("/var/log/syslog.1", timestamp_format=fmt2)
    log2 = LogFile("/var/log/auth.log.1", timestamp_format=fmt2)
    #log2 = LogFile("/var/log/dpkg.log", timestamp_format=fmt3)
    print(match)
    print(match1)

    eventmatch = match_events(log1, log2, primary_contents='Error', before=6, after=0)
    #eventmatch = match_events(log1, log2, before=6, after=6)

    for k, v in eventmatch.items():
        print(k)
        print('\t', v[0][0])
        print('\t'.join(v[1]))

import unittest
from datetime import datetime
from List2.analyzeLog import analyze_log
from List2.countByMethod import count_by_method
from List2.countStatusClasses import count_status_classes
from List2.detectSus import detect_sus
from List2.entryToDict import entry_to_dict
from List2.getEntriesByAddr import get_entries_by_addr
from List2.getEntriesByCode import get_entries_by_code
from List2.getEntriesByExtension import get_entries_by_extension
from List2.getEntriesInTimeRange import get_entries_in_time_range
from List2.getFailedReads import get_failed_reads
from List2.getMostActiveSession import get_most_active_session
from List2.getExtensionStats import get_extension_stats
from List2.getSessionPaths import get_session_paths
from List2.getTopIPs import get_top_ips
from List2.getTopURIs import get_top_uris
from List2.getUniqueMethods import get_unique_methods
from List2.logToDict import log_to_dict
from List2.readLog import read_log
from List2.sortLog import sort_log, sort_log_by_name

TEST_FILE_PATH = 'List2/utils/http_first_100k.log'
INVALID_TEST_FILE_PATH = 'data/tests/test_invalid.log'


log = []

try:
    with open(TEST_FILE_PATH, 'r') as file:
        log = read_log(file)
except FileNotFoundError:
    raise ValueError('Error: That file does not exist.')




class TestLab03(unittest.TestCase):
    def test_zad1(self):
        self.assertEqual(len(log), 100000)
        self.assertIsInstance(log[0][0], datetime)
        self.assertIsInstance(log[0][9], int)

    def test_zad2(self):
        # Sortowanie po indeksie
        sorted_by_ts = sort_log(log, 0)
        self.assertLessEqual(sorted_by_ts[0][0], sorted_by_ts[-1][0])

        with self.assertRaises(IndexError):
            sort_log(log, 999)

        # Sortowanie po nazwie pola
        sorted_by_method = sort_log_by_name(log, 'method')
        self.assertEqual(sorted_by_method[0].method, sorted_by_method[0].method)

        with self.assertRaises(AttributeError):
            sort_log_by_name(log, 'nieistniejace_pole')

    def test_zad3(self):
        # Standardowe działanie
        entries_200 = get_entries_by_code(log, 200)
        self.assertIsInstance(entries_200, list)
        if entries_200:
            self.assertEqual(entries_200[0].status_code, 200)

        # Oczekiwany błąd typu
        with self.assertRaises(TypeError):
            get_entries_by_code(log, '200')

    def test_zad4(self):
        # Prawidłowy adres
        entries = get_entries_by_addr(log, '192.168.1.1')
        self.assertIsInstance(entries, list)

        # Nieprawidłowy typ
        with self.assertRaises(TypeError):
            get_entries_by_addr(log, 12345)

        # Nieprawidłowy format IP
        with self.assertRaises(ValueError):
            get_entries_by_addr(log, '999.999.999.999')

    def test_zad5(self):
        # Test bez łączenia
        tuple_result = get_failed_reads(log, merge=False)
        self.assertIsInstance(tuple_result, tuple)
        self.assertEqual(len(tuple_result), 2)
        self.assertIsInstance(tuple_result[0], list)
        self.assertIsInstance(tuple_result[1], list)

        # Test z łączeniem
        list_result = get_failed_reads(log, merge=True)
        self.assertIsInstance(list_result, list)

    def test_zad6(self):
        # Sprawdzenie odporności na brak kropki oraz wielkość liter
        entries_jpg = get_entries_by_extension(log, 'jpg')
        entries_dot_jpg = get_entries_by_extension(log, '.JPG')

        self.assertIsInstance(entries_jpg, list)
        # Powinny zwrócić tę samą liczbę elementów
        self.assertEqual(len(entries_jpg), len(entries_dot_jpg))

    def test_zad7(self):
        # Prawidłowe działanie
        top_ips = get_top_ips(log, n=5)
        self.assertIsInstance(top_ips, list)
        self.assertLessEqual(len(top_ips), 5)
        if top_ips:
            self.assertIsInstance(top_ips[0], tuple)

        # Walidacja danych wejściowych
        with self.assertRaises(TypeError):
            get_top_ips(log, n=-1)
        with self.assertRaises(TypeError):
            get_top_ips(log, n='5')

    def test_zad8(self):
        methods = get_unique_methods(log)
        self.assertIsInstance(methods, list)

        # Sprawdzenie czy nie ma duplikatów
        self.assertEqual(len(methods), len(set(methods)))

        if methods:
            self.assertIsInstance(methods[0], str)

    def test_zad9(self):
        if log:
            # Bierzemy czas z pierwszego i setnego logu
            start_ts = log[0].ts
            end_ts = log[100].ts

            entries = get_entries_in_time_range(log, start_ts, end_ts)
            self.assertIsInstance(entries, list)
            # Powinno znaleźć przynajmniej ten pierwszy
            self.assertGreater(len(entries), 0)

            # Walidacja typów daty
        with self.assertRaises(TypeError):
            get_entries_in_time_range(log, 'zła_data', 'gorsza_data')

    def test_zad10(self):
        counts = count_by_method(log)
        self.assertIsInstance(counts, dict)

        if counts:
            first_key = list(counts.keys())[0]
            self.assertIsInstance(first_key, str)
            self.assertIsInstance(counts[first_key], int)

    def test_zad11(self):
        top_uris = get_top_uris(log, n=1)
        self.assertEqual(len(top_uris), 1)
        self.assertIsInstance(top_uris[0], tuple)
        self.assertEqual(top_uris[0][1], 8354)

        with self.assertRaises(TypeError):
            get_top_uris(log, n='five')

    def test_zad12(self):
        stats = count_status_classes(log)
        self.assertEqual(stats['2xx'], 13020)
        self.assertEqual(stats['4xx'], 78919)
        self.assertEqual(stats['5xx'], 1592)

        with self.assertRaises(TypeError):
            count_status_classes('not_list')

    def test_zad13(self):
        d = entry_to_dict(log[0])
        self.assertIsInstance(d, dict)
        self.assertEqual(d['id_orig_h'], '192.168.202.79')
        self.assertEqual(d['method'], 'HEAD')

        with self.assertRaises(ValueError):
            entry_to_dict((1, 2, 3))

    def test_zad14(self):
        log_dict = log_to_dict(log)
        self.assertIsInstance(log_dict, dict)
        for uid in log_dict:
            self.assertIsInstance(log_dict[uid], list)
            self.assertIsInstance(log_dict[uid][0], dict)

    # def test_zad15(self):
    #     log_dict = log_to_dict(log)
    #     try:
    #         print_dict_entry_dates(log_dict)
    #     except Exception as e:
    #         self.fail(f'print_dict_entry_dates casted error: {e}')
    #
    #     with self.assertRaises(TypeError):
    #         print_dict_entry_dates('no_dict')

    def test_zad16(self):
        result = get_most_active_session(log)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        self.assertIsInstance(result[1], int)
        self.assertGreater(result[1], 0)

        # self.assertIsNone(get_most_active_session({}))

        with self.assertRaises(TypeError):
            get_most_active_session('not_a_log')

    def test_zad17(self):
        paths = get_session_paths(log)
        self.assertIsInstance(paths, dict)

        if paths:
            first_uid = list(paths.keys())[0]
            self.assertIsInstance(paths[first_uid], list)

            self.assertIsInstance(paths[first_uid][0], str)

    def test_zad18(self):
        suspicious = detect_sus(log, threshold=100)
        self.assertIsInstance(suspicious, dict)

        suspicious_low = detect_sus(log, threshold=5)
        self.assertIsInstance(suspicious_low, dict)

        #BŁĘDNE WARTOŚCI
        with self.assertRaises(ValueError):
            detect_sus(log, threshold=0)

        with self.assertRaises(ValueError):
            detect_sus(log, threshold=-10)

        with self.assertRaises(ValueError):
            detect_sus(log, threshold='high')

        with self.assertRaises(ValueError):
            detect_sus(log, threshold=5.5)

    def test_zad19(self):
        stats = get_extension_stats(log)
        self.assertIsInstance(stats, dict)

        for ext in stats.keys():
            self.assertNotIn('.', ext)
            self.assertNotIn('/', ext)

        # print(stats)

    def test_zad20(self):
        report = analyze_log(log)

        self.assertIsInstance(report, dict)
        expected_keys = [
            'most_used_ip', 'most_used_uri', 'method_distribution', 'error_count', 'total_requests'
        ]
        for key in expected_keys:
            self.assertIn(key, report)
        self.assertIsInstance(report['error_count'], int)

        print('\n' + '=' * 40)
        print('       FINAL LOG ANALYSIS REPORT')
        print('=' * 40)
        print(f'Total Requests:      {report['total_requests']}')
        print(f'Error Count (4xx+5xx): {report['error_count']}')

        if report['most_used_ip']:
            ip, count = report['most_used_ip']
            print(f'Most Active IP:      {ip} ({count} reqs)')

        if report['most_used_uri']:
            uri, count = report['most_used_uri']
            print(f'Most Popular URI:    {uri} ({count} reqs)')

        print('\nMethod Distribution:')
        for method, count in report['method_distribution'].items():
            print(f'  - {method}: {count}')

if __name__ == '__main__':
    unittest.main(exit=False)
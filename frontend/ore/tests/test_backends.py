import unittest
import sys
import json

from ore.models import Graph, Job, Result
from .common import fixt_analysis, fixt_mincut, OreLiveServerTestCase


class BackendDaemonTestCase(OreLiveServerTestCase):

    """
        Base class for tests of backend functionality.
        This demands firing up the backend daemon in the setup phase, which
        is done here.
    """

    baseUrl = '/api/front'

    def setUp(self):
        # Start up backend daemon in testing mode so that it uses port 8081 of
        # the live test server
        # print "Starting backend daemon"
        # os.chdir("/ore-back")
        # self.backend = subprocess.Popen(["python", "daemon.py", "--force_server", self.live_server_url])
        # time.sleep(2)
        # os.chdir("..")
        self.setUpLogin()

#    def tearDown(self):
#        print "\nShutting down backend daemon"
        # self.backend.terminate()


class InternalTestCase(BackendDaemonTestCase):

    """
        The tests for internal functions that are not exposed directly via one of the APIs.
        Since some tests explicitely create job objects, a signal is always triggered to talk to
        the backend daemon. For this reason, we need to fire it up.
        #TODO: This is no longer needed when Django supports signal disabling in tests.
    """
    fixtures = fixt_analysis['files']

    def test_result_parsing(self):
        for graphPk, graphResult in fixt_analysis['results'].iteritems():
            graph = Graph.objects.get(pk=graphPk)
            job = Job(
                graph_modified=graph.modified,
                graph=graph,
                kind=Job.TOP_EVENT_JOB)
            job.save()
            job.parse_result(open('ore/fixtures/' + graphResult).read())
            for result in job.results.exclude(kind__exact=Result.GRAPH_ISSUES):
                print "Result"
                print result


class AnalysisFixtureTestCase(BackendDaemonTestCase):

    """
        Analysis engine tests.
    """
    fixtures = fixt_analysis['files']

    @unittest.skipUnless(
        sys.platform.startswith("linux"), "requires Linux")
    def testRateFaulttree(self):
        job_result = self.requestJob(
            self.baseUrl,
            fixt_analysis['rate_faulttree'],
            'topevent')
        job_result_info = json.loads(job_result.content)
        assert('issues' in job_result_info)
        assert('columns' in job_result_info)
        result_url = job_result['LOCATION']
        result = self.ajaxGet(
            result_url +
            '?sEcho=doo')   # Fetch result in datatables style
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.content)
        self.assertEqual(data['aaData'][0]['peak'], 1.0)

    @unittest.skipUnless(
        sys.platform.startswith("linux"), "requires Linux")
    def testRateFaulttreeSimulation(self):
        job_result = self.requestJob(
            self.baseUrl,
            fixt_analysis['rate_faulttree'],
            'simulation')
        result_url = job_result['LOCATION']
        result = self.ajaxGet(
            result_url +
            '?sEcho=doo')   # Fetch result in datatables style
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.content)
        assert(len(data['aaData']) > 0)

    @unittest.skipUnless(
        sys.platform.startswith("linux"), "requires Linux")
    def testPRDCFuzztree(self):
        job_result = self.requestJob(
            self.baseUrl,
            fixt_analysis['prdc_fuzztree'],
            'topevent')
        job_result_info = json.loads(job_result.content)
        assert('issues' in job_result_info)
        assert('columns' in job_result_info)
        print "\n" + str(job_result_info)
        result_url = job_result['LOCATION']
        result = self.ajaxGet(
            result_url +
            '?sEcho=doo')  # Fetch result in datatables style
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.content)
        print "\n" + str(data)
        self.assertEqual(
            len(data['aaData']), fixt_analysis['prdc_configurations'])
        for conf in data['aaData']:
            assert (round(conf['peak'], 5) in fixt_analysis['prdc_peaks'])

    def testFrontendAPIPdfExport(self):
        for graphPk, graphType in fixt_analysis['graphs'].iteritems():
            job_result = self.requestJob(self.baseUrl, graphPk, 'pdf')
            pdf_url = job_result['LOCATION']
            pdf = self.get(pdf_url)
            self.assertEqual('application/pdf', pdf['CONTENT-TYPE'])

    @unittest.skipUnless(
        sys.platform.startswith("linux"), "requires Linux")
    def testFrontendAPIEpsExport(self):
        for graphPk, graphType in fixt_analysis['graphs'].iteritems():
            job_result = self.requestJob(self.baseUrl, graphPk, 'eps')
            eps_url = job_result['LOCATION']
            eps = self.get(eps_url)
            self.assertEqual('application/postscript', eps['CONTENT-TYPE'])

    @unittest.skipUnless(
        sys.platform.startswith("linux"), "requires Linux")
    def testResultOrdering(self):
        job_result = self.requestJob(
            self.baseUrl,
            fixt_analysis['prdc_fuzztree'],
            'topevent')
        result_url = job_result['LOCATION']
        # Ordering in datatables style
        titles = Result.titles(Result.ANALYSIS_RESULT, 'fuzztree')
        print "\nFields being supported in the result: %s\n" % str(titles)
        for index, col_desc in enumerate(
                titles, start=0):      # Datatables starts at column 1
            field_name = col_desc[0]
            print "Fetching result sorted by " + field_name
            url = result_url + \
                '?sEcho=doo&iSortingCols=1&sSortDir_0=asc&iSortCol_0=' + \
                str(index)
            result = self.ajaxGet(url)
            data = json.loads(result.content)
            for i in xrange(0, len(data['aaData']), 2):
                prec = data['aaData'][i][field_name]
                succ = data['aaData'][i + 1][field_name]
                print prec
                print succ
                assert(prec <= succ)


class MinCutFixtureTestCase(BackendDaemonTestCase):

    """
        Mincut engine tests.
    """
    fixtures = fixt_mincut['files']

    @unittest.skip("")
#    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux")
    def testMincutFaulttree(self):
        job_result = self.requestJob(
            self.baseUrl,
            fixt_mincut['mincut_faulttree'],
            'mincut')
        result_url = job_result['LOCATION']
        result = self.ajaxGet(
            result_url +
            '?sEcho=doo')   # Fetch result in datatables style
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.content)
        assert(len(data['aaData']) > 0)
        assert('mincutResults' in data['aaData'][0])
        mincut_results = data['aaData'][0]['mincutResults']
        self.assertEqual(len(mincut_results), fixt_mincut['mincut_numcuts'])

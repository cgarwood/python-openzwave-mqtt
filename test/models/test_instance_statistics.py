def test_statistics(mgr):
    RESPONSE_JSON = {
        "SOFCnt": 148,
        "ACKWaiting": 0,
        "readAborts": 0,
        "badChecksum": 1,
        "readCnt": 147,
        "writeCnt": 29,
        "CANCnt": 0,
        "NAKCnt": 0,
        "ACKCnt": 29,
        "OOFCnt": 0,
        "dropped": 0,
        "retries": 0,
        "callbacks": 0,
        "badroutes": 0,
        "noack": 7,
        "netbusy": 0,
        "notidle": 0,
        "txverified": 0,
        "nondelivery": 0,
        "routedbusy": 0,
        "broadcastReadCnt": 46,
        "broadcastWriteCnt": 9,
    }

    mgr.mock_receive_json("OpenZWave/1", {})
    mgr.mock_receive_json("OpenZWave/1/statistics/", RESPONSE_JSON)
    statistics = mgr.get_instance("1").get_statistics()
    assert statistics.sof_count == 148
    assert statistics.read_count == 147
    assert statistics.write_count == 29
    assert statistics.net_busy == 0

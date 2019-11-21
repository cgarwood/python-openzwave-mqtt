def test_statistics(mgr):
    RESPONSE_JSON = {
        "ackChannel": 0,
        "averageRequestRTT": 31,
        "averageResponseRTT": 47,
        "extendedTXSupported": False,
        "hops": 0,
        "lastFailedLinkFrom": 0,
        "lastFailedLinkTo": 0,
        "lastRecievedTimeStamp": 0,
        "lastRequestRTT": 29,
        "lastResponseRTT": 44,
        "lastSentTimeStamp": 0,
        "lastTXChannel": 0,
        "quality": 0,
        "receivedDupPackets": 3,
        "receivedPackets": 109,
        "receivedUnsolicited": 98,
        "retries": 0,
        "routeScheme": "Idle",
        "routeSpeed": "Auto",
        "routeTries": 0,
        "routeUsed": "",
        "route_1": 0,
        "route_2": 0,
        "route_3": 0,
        "route_4": 0,
        "rssi_1": "",
        "rssi_2": "",
        "rssi_3": "",
        "rssi_4": "",
        "rssi_5": "",
        "sendCount": 10,
        "sentFailed": 0,
        "txTime": 0,
    }

    mgr.mock_receive_json("openzwave/1", {})
    mgr.mock_receive_json("openzwave/1/node/2", {})
    mgr.mock_receive_json("openzwave/1/node/2/statistics/", RESPONSE_JSON)
    statistics = mgr.get_instance("1").get_node("2").get_statistics()
    assert statistics.ack_channel == 0
    assert statistics.average_response_rtt == 47
    assert statistics.average_request_rtt == 31
    assert statistics.send_count == 10
    assert statistics.parent.id == "2"

var controls_cont = $('#mktwcontrols');
var nv_cont_list = $('#mktwheadlines').find('ol');
var filter_criteria = controls_cont.find('.tabs a.selected').attr('name');
var headline_url = '/newsviewer/mktwheadlines'
var older_items_pullcount = 1000;

var mkt_page_params = function(criteria) {			
    return  {
        topstories: (criteria=='topstories' || criteria=='latest'),
        rtheadlines: (criteria=='rtheadlines' || criteria=='latest'),
        pulse: (criteria=='pulse' || criteria=='latest'),
        commentary: (criteria=='latest' || criteria=='latest'),
        video: (criteria=='latest'),
        zmgVideo: (criteria=='latest'),
        premium: (criteria=='latest'),
        blogs: (criteria=='blogs' || criteria=='latest'),
        topic: 'All Topics'	
    };			
};

var get_params = mkt_page_params;


var getItem = function (selector) {
    return nv_cont_list.find(selector);
};

var lastHeadline = function () {
    var item = getItem('li:last');
    if (item.hasClass('loading')) //don't want to return the load indicator
        item = item.prev();

    return item;
};

var GetPartialViewPost = function (url, page_params, callback) {
    $.ajax({
        type: "POST",
        url: url,
        data: page_params,
        dataType: "html",
        global: "false",
        success: function (data) {
            callback(data);
        }
    });
};

var GetOlderHeadlines = function () {

    var doc_id = lastHeadline().attr('id');
    var time_stamp = lastHeadline().attr('timestamp');
    var ajax_params = {};

    $.extend(ajax_params, get_params(filter_criteria), {
        docId: doc_id,
        timestamp: time_stamp,
        pullCount: older_items_pullcount
    });

    //make ajax call and execute callback
    GetPartialViewPost(
        headline_url,
        ajax_params,
        function (partial_view) {
            GetOlderHeadlinesCompleted(partial_view);
        }
    );
};

var GetOlderHeadlinesCompleted = function (partial_view) {
    nv_cont_list.append(partial_view);
    InitializeViewPort(false, false, true);
};

var loadIndicator = function () {
    return getItem('li.loading');
};

var ResetLoadIndicator = function () {
    loadIndicator().remove();
    lastHeadline().after("<li class='loading'><img src='../Content/images/ajax-loader.gif' />Loading more headlines...</li>");
};

var InitializeViewPort = function (highlight_default, enforce_max, init_bluegrass) {
    // Remove any items if the viewer is beyond it's max
    //if (enforce_max)
    //    getItem('li:gt(' + (max_viewer_items - 1) + ')').remove();
    ResetLoadIndicator();

};

GetOlderHeadlines();
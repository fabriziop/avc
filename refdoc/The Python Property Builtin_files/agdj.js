$(function(){
        filter_homepage();
        humanize_timestamps();
        nospam_comments();
  });

function filter_homepage(){
    $(".feedlist input").change(function(){
        var items = $("article[data-feed-id="+$(this).parent().attr("data-feed-id")+"]");
        if($(this).attr("checked")){
            items.show();
        }else{
            items.hide();
        }
    }).change();
    }

function humanize_timestamps(){
    $(".comment .humanize.iso8601").each(comment_timestamp_update);
    $("#metadata > .humanize.iso8601").each(timestamp_update);
    $(".humanize.iso8601").each(timestamp_update);
    $("time").each(timetag_update);
}

function timestamp_humanize(dt){
    return timediff_humanize(new Date(), dt)+" ago";
}

function timelater_humanize(post_dt, comment_dt){
    return timediff_humanize(post_dt, comment_dt)+" later";
}

function comment_timestamp_update(){
    var post_dt = timestamp_parse($("#metadata .iso8601").html());
    var current_timestamp = $(this).html();
    var comment_dt = timestamp_parse(current_timestamp);
    var new_date_string = timelater_humanize(post_dt, comment_dt);
    $(this).attr("title", current_timestamp);
    $(this).html(new_date_string);
    $(this).removeClass("humanize");
}

function timestamp_update(){
    var current_timestamp = $(this).html();
    var new_date_string = timestamp_humanize(timestamp_parse(current_timestamp));
    $(this).attr("title", current_timestamp);
    $(this).html(new_date_string);
    $(this).removeClass("humanize");
}

function timetag_update(){
    var current_timestamp = $(this).attr("datetime");
    var new_date_string = timestamp_humanize(timestamp_parse(current_timestamp));
    $(this).html(new_date_string);
}

function timestamp_parse(timestamp){
    var represented_date = new Date();
    /* Example date: "2008-03-03T15:28:36Z" */
    var iso8601_parser = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z$/;
    // Note the splice to remove the first group, which is the entire
    // string.
    var str_groups = timestamp.match(iso8601_parser).splice(1);
    int_groups = [];
    for(var ii in str_groups)
        int_groups.push(parseInt(str_groups[ii], 10));
    represented_date.setUTCFullYear(int_groups[0]);
    represented_date.setUTCMonth(int_groups[1]-1);
    represented_date.setUTCDate(int_groups[2]);
    represented_date.setUTCHours(int_groups[3]);
    represented_date.setUTCMinutes(int_groups[4]);
    represented_date.setUTCSeconds(int_groups[5]);
    return represented_date;
}

function timediff_humanize(dt1, dt2){
    var diff_millisecs = Math.abs(dt1.getTime() - dt2.getTime());
    var diff_secs = Math.round(diff_millisecs / 1000);
    var minute = 1 * 60;
    var hour = minute * 60;
    var day = hour * 24;
    var week = day * 7;
    var month = week * 4;
    var year = month * 12;

    if(diff_secs<minute){
        return "less than a minute";
    }else if(diff_secs<2*hour){
        return pluralize(" minute", Math.round(diff_secs/minute));
    }else if(diff_secs<2*day){
        return pluralize(" hour", Math.round(diff_secs/hour));
    }else if(diff_secs<2*week){
        return pluralize(" day", Math.round(diff_secs/day));
    }else if(diff_secs<2*month){
        return pluralize(" week", Math.round(diff_secs/week));
    }else if(diff_secs<2*year){
        return pluralize(" month", Math.round(diff_secs/month));
    }
    return pluralize(" year", Math.round(diff_secs/year));
}

function pluralize(string, number){
    if(number==1){
        return "one"+string;
    }else{return number+string+"s";}
}

function nospam_comments(){
    // Change the form here in JS code so that bots don't do it
    // right. It still works without this, just doesn't show up until
    // it's manually approved
    $(".comments .add.nospam-me").each(modify_keys_nospam);
}

function modify_keys_nospam(){
    $(this).append('<input type="hidden" name="not_spam" value="indeed." />');
}


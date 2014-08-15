

function ajax_delete_article(id_art,domElem){
   
    $.ajax({
        type:"POST",
        url: 'delete_article/',
        data:{id_art:id_art,},
    })
    .done(function(response) {
        if (response) {
            domElem.remove()
        }
    })
    .fail(function() {
      alert( "error when trying to delete." );
    });
 
}

function make_article_form(url,domElem){
    
     $.ajax({
        type:"GET",
        url: url,
    })
    .done(function(response) {
        domElem.find('.article').hide();     
        domElem.prepend(response);
        domElem.find("textarea").addClass('summernote');
        domElem.find("textarea").summernote({
            height: 300,                 // set editor height
            minHeight: null,             // set minimum height of editor
            maxHeight: null,             // set maximum height of editor
            focus: true,                 // set focus to editable area after initializing summernote
          });
    })
    .fail(function() {
      alert( "error when trying to get article form." );
    });
}

function make_article_html(authenticated,article){
    
    var li="";
        if(authenticated) {
            li=li+
            '<li art-id="'+article.id+'">'+
                '<div class="article">'+
                    '<div class="article_head">'+
                        '<div title="Delete" class="remove">'+
                            '<img src="https://cdn2.iconfinder.com/data/icons/flat-ui-icons-24-px/24/cross-24-128.png">'+
                        '</div>'+
                        '<div title="Edit" class="edit">'+
                           '<img src="https://cdn2.iconfinder.com/data/icons/flat-ui-icons-24-px/24/new-24-128.png">'+
                        '</div>'+
                        '<h2>'+article.title+'</h2>'+
                        '<div class="published"><span class="caption">Posted:</span>'+
                            '<span class="publishdate" itemprop="datePublished">'+article.created+'</span>'+
                        '</div>'+
                    '</div>'+
                    '<div class="article_content">'+
                        article.content+
                    '</div>'+
                '</div>'+
            '</li>';
        } else {
            li=li+
            '<li art-id="'+article.id+'">'+
                '<div class="article">'+
                    '<div class="article_head">'+
                        '<h2>'+article.title+'</h2>'+
                        '<div class="published"><span class="caption">Posted:</span>'+
                            '<span class="publishdate" itemprop="datePublished">'+article.created+'</span>'+
                        '</div>'+
                    '</div>'+
                    '<div class="article_content">'+
                        article.content+
                    '</div>'+
                '</div>'+
            '</li>';
        }
    return li
}

function get_article(url_dir,atr_id)
{
    $.ajax({
        type:"POST",
        url: url_dir,
        data:{id:atr_id,},
    })
    .done(function(response) {
        var json_response = jQuery.parseJSON(response);
        var articles= json_response['articles'];
        var authenticated =json_response['authenticated']
        var li = '';
        if ($('.scrollable [art-id='+articles[0].id+']').length > 0) {
            $('.scrollable [art-id='+articles[0].id+']').remove()
        }
        li = make_article_html(authenticated, articles[0])
        $(".scrollable").prepend(li);
        jQuery('html, body').animate( { scrollTop: 0 }, 'slow' );
    })
}


function ajax_infinite_scroll(url_dir){

    /**** get articles by ajax and append to the page ******/
    last_id=$(".scrollable > :last-child").attr('art-id');
    $.ajax({
        type:"POST",
        url: url_dir,
        data:{last_id:last_id,},
    })
    .done(function(response) {
        var json_response = jQuery.parseJSON(response);
        var articles= json_response['articles'];
        var authenticated =json_response['authenticated']
        var li = '';
        for(i=0; i< articles.length; i++) {
            if ($('.scrollable [art-id='+articles[i].id+']').length == 0) {
              li = li + make_article_html(authenticated, articles[i])
            }
        }
        $(".scrollable").append(li);
        
    })
    .fail(function() {
      alert( "error when trying to save." );
    });
};

/*****************Click events***************************************/
$(document).on("click",".filtered_article",function(e){
    
    var domElement = $(e.target);
    var id_art = domElement.attr('art-id');
    var url='get_article/'
    get_article(url,id_art);
    });

$(document).on("click","#new_article",function(){
    var domElement = $('.scrollable');
    url='do_article/';
    li = $('<li>');
    make_article_form(url,li);
    domElement.prepend(li);
});

$(document).on("click",".remove",function(e){
    var domElement = $(e.target);
    var id_art = domElement.closest('li').attr('art-id');
    ajax_delete_article(id_art,domElement.closest('li'));
    });

$(document).on("click",".edit",function(e){
    
    var domElement = $(e.target);
    var id_art = domElement.closest('li').attr('art-id');
    url='do_article/?art_id='+id_art
    make_article_form(url,domElement.closest('li'));
    
    });

$(document).on("click",".submit",function(e){
    var domElement = $(e.target);
    li = domElement.closest("li");
    li.find('#article_form').submit();
});

$(document).on("click",".cancel",function(e){
    var domElement = $(e.target);
    li = domElement.closest("li");
    li.find('.article').show();
    li.find('#article_form').remove();
});

var toggleMonths = function() {
    $(".collapse_month").slideToggle();
}

var toggleArticles = function() {
    $(".collapse_article").slideToggle();
}


$(document).ready(function() {
   var last_id='';
   var ref='/pull_articles/';
    $(window).scroll(function(e)
    {
       // if at bottom, add new content:
       if  ($(window).scrollTop() == $(document).height() - $(window).height())
       {
            ajax_infinite_scroll(ref);
       }
    });
    $(".collapse_article").hide();
    $(".collapse_month").hide();
});


   
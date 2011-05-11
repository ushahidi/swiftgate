/*
 * Setup functions for jQuery based actions
 */
$(document).ready
(
    function()
    {
        //Set up expandable areas
        $(".expandable").each(function(){Expandable($(this))});
    }
);

function Expandable(subject)
{
    if($(subject).is('.show'))
    {
        $(subject).append("<a class='collapsible-trigger'><img src='" + baseUrl + "static/images/icon-collapse.png' /></a>");
        $(subject).find("a.collapsible-trigger").click(function(){Collapse($(this))});
    }
    else
    {
        $(subject).prepend("<a class='expandable-trigger'><img src='" + baseUrl + "static/images/icon-expand.png' /></a>");
        $(subject).find("a.expandable-trigger").click(function(){Expand($(this))});
    }
    
}

function Expand(subject)
{
    $(subject).parent().find('.expandable-inner').slideDown();
    $(subject).slideUp()
    $(subject).parent().append("<a class='collapsible-trigger'><img src='" + baseUrl + "static/images/icon-collapse.png' /></a>");
    $(subject).parent().find("a.collapsible-trigger").click(function(){Collapse($(this))});
}

function Collapse(subject)
{
    $(subject).parent().find('.expandable-inner').slideUp();
    $(subject).slideUp()
    $(subject).parent().prepend("<a class='expandable-trigger'><img src='" + baseUrl + "static/images/icon-expand.png' /></a>");
    $(subject).parent().find("a.expandable-trigger").click(function(){Expand($(this))});
}

function AppTemplateOnChange()
{
    var selectedValue = $('#appTemplateSelect').val();
    $('#app-template-descriptions').children().slideUp();
    if(selectedValue != '0')
        $('#app-template-descriptions #' + selectedValue.replace('/', '_')).slideDown();
}

function AddAppChoosePricePlanButtonClick()
{
    $('#add-app-more-details-button').slideUp();
    $('#add-app-more-details').slideDown()
}

function RevealAppSecret()
{
    $('#app-secret-action').slideUp(function(){
        $('#app-secret').slideDown();
    });
}
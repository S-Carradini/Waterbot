"use strict";

$(document).ready(function () {
  $('.toast').toast('hide');
  $('.waterdrop1').popover('hide');
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  }); // Function to display a user message in the chat interface

  function displayUserMessage(userQuery) {
    var chatHistory = document.getElementById('chatbot-prompt');
    var userMessage = document.createElement('div');
    userMessage.classList.add('card', 'user-message', 'right');
    userMessage.innerHTML = "\n\n        <div class=\"card-body chatbot-question\">\n          <div class=\"row\">             \n            <div class=\"col-xs-12 col-sm-12 col-md-10 col-lg-10 col-xl-10 col-10 message-body\">\n            ".concat(userQuery, "\n            </div>\n            \n          </div>\n        </div>\n\n      ");
    chatHistory.appendChild(userMessage);
  }

  function showReactions(message) {
    $(message).find('.reactions').show();
  }

  function hideReactions(message) {
    $(message).find('.reactions').hide();
  }

  function completeRequest() {
    $('.toast').toast('show');
  }

  function submitReaction($clickedReaction) {
    var reactionValue = $clickedReaction.data('reaction');
    console.log("Sending reaction: " + reactionValue);
    var messageID = $clickedReaction.attr("data-messageid");
    if (reactionValue == 0) $("#modal-" + messageID).find(".modal-header >i").removeClass("bi bi-hand-thumbs-up").addClass("bi bi-hand-thumbs-down"); // Send a POST request with the selected reaction and message

    fetch('/submit_rating_api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        'reaction': reactionValue,
        'message_id': messageID
      })
    }).then(function (response) {
      return response.text();
    }).then(function (message) {
      console.log(message); // Handle the response as needed

      $("button.comment[data-messageid=" + messageID + "]").attr("data-reaction", reactionValue);
    });
  }

  function submitComment($clickedReaction) {
    var reactionValue = $clickedReaction.data('reaction');
    var messageID = $clickedReaction.parent().parent().find("button.comment").attr("data-messageid");
    var commentInput = $clickedReaction.parent().parent().find('#userComment-' + messageID).val();
    var feedbackMsg = "\n    <div class=\"card-footer\">\n    <div class=\"row\">\n      <div class=\"col-1\"></div>\n      <div class=\"col-11\">\n        <span class=\"feedback-".concat(messageID, "\" data-messageid=\"").concat(messageID, "\">Thanks for your feedback</span>     \n      </div>\n      </div>\n    </div>");
    console.log("Sending comment: " + commentInput + " for " + messageID); // Send a POST request with the selected reaction and message

    fetch('/submit_rating_api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        'userComment': commentInput,
        'message_id': messageID
      })
    }).then(function (response) {
      return response.text();
    }).then(function (message) {
      console.log(message); // Handle the response as needed
      //Remove one of the reactions

      if (reactionValue == "1") {
        //means thumbs-up
        //remove thumbs-down
        $("span.reaction[data-reaction='0'][data-messageid=" + messageID + "]").remove(); //Remove click event from thumbs up

        $("span.reaction[data-reaction='1'][data-messageid=" + messageID + "]").removeAttr("data-bs-toggle");
        $("span.reaction[data-reaction='1'][data-messageid=" + messageID + "]").removeAttr("data-bs-target"); //Replace the icon to fill
        //$("span.reaction[data-reaction='1'][data-messageid="+messageID+"] > i").removeClass("bi-hand-thumbs-up").addClass("bi-hand-thumbs-up-fill");

        $("span.reaction[data-reaction='1'][data-messageid=" + messageID + "] > i").addClass("reaction-feedback");
        $("span.reaction[data-reaction='1'][data-messageid=" + messageID + "]").removeClass("reaction");
      } else {
        //remove thumbs-up
        $("span.reaction[data-reaction='1'][data-messageid=" + messageID + "]").remove(); //Remove click event from thumbs up

        $("span.reaction[data-reaction='0'][data-messageid=" + messageID + "]").removeAttr("data-bs-toggle");
        $("span.reaction[data-reaction='0'][data-messageid=" + messageID + "]").removeAttr("data-bs-target"); //Replace the icon to fill
        //$("span.reaction[data-reaction='0'][data-messageid="+messageID+"] > i").removeClass("bi-hand-thumbs-down").addClass("bi-hand-thumbs-down-fill");

        $("span.reaction[data-reaction='0'][data-messageid=" + messageID + "] > i").addClass("reaction-feedback");
        $("span.reaction[data-reaction='0'][data-messageid=" + messageID + "]").removeClass("reaction");
      } //Close the modal popup


      $("#modal-" + messageID).modal('toggle');
      $(".card.data-messageid-" + messageID).append(feedbackMsg);
      scrollToBottom(); //   $('#waterdropFeedback').popover('show');
      //   setTimeout(function () {
      //     $('#waterdropFeedback').popover('hide');
      // }, 2000);
      //completeRequest();
    });
  } // Function to display a bot message in the chat interface


  function displayBotMessage(botResponse, messageID) {
    var chatHistory = document.getElementById('chatbot-prompt');
    var botMessage = document.createElement('div');
    botMessage.classList.add('card', 'left');
    botMessage.classList.add('card', 'bot-message', 'data-messageid-' + messageID);
    botMessage.innerHTML = "\n        <div class=\"card-body welcome-message pb-0\" data-messageid=".concat(messageID, ">\n        <div class=\"row\">\n          <div class=\"col-xs-12 col-sm-12 col-md-2 col-lg-2 col-xl-2 col-2 d-flex flex-wrap align-items-center justify-content-center\">\n            <img class=\"waterdrop1\" />\n          </div>\n          <div class=\"col-xs-12 col-sm-12 col-md-10 col-lg-10 col-xl-10 col-10 bot-message-body\">\n            <span>").concat(botResponse, "</span>\n          </div>\n          \n          </div>\n        </div>\n        <div class=\"card-footer\" style=\"padding:8px; border:0;\">\n          <div class=\"row\">\n            <div class=\"col-2\"></div>\n            <div class=\"col-10\">\n              <span class=\"reaction\" data-toggle=\"tooltip\" data-placement=\"top\" title=\"Good response\" data-bs-toggle=\"modal\" data-messageid=").concat(messageID, " data-bs-target=\"#modal-").concat(messageID, "\" data-reaction=\"1\"><i class=\"bi bi-hand-thumbs-up fa-1x\"></i></span>  \n              <span class=\"reaction\" data-toggle=\"tooltip\" data-placement=\"top\" title=\"Could be better\" data-bs-toggle=\"modal\" data-messageid=").concat(messageID, " data-bs-target=\"#modal-").concat(messageID, "\" data-reaction=\"0\"><i class=\"bi bi-hand-thumbs-down fa-1x\"></i></span>\n              <!-- <button type=\"button\" class = \"followup-buttons\" id=\"shortButton\">\n              <div>Short</div>\n            </button>  -->\n            <button type=\"button\" class = \"followup-buttons\" id=\"detailedButton\">\n              <div>Detailed</div>\n            </button>\n            <button type=\"button\" class = \"followup-buttons\" id=\"actionItemsButton\">\n              <div>Next steps</div>\n            </button>\n            <button type=\"button\" class = \"followup-buttons\" id=\"sourcesButton\">\n              <div>Source</div>\n            </button>\n            </div>\n          </div>\n        </div>\n\n        <!-- Modal -->\n        <div class=\"modal fade\" id=\"modal-").concat(messageID, "\" tabindex=\"-1\" aria-labelledby=\"exampleModalLabel\" aria-hidden=\"true\">\n          <div class=\"modal-dialog modal-dialog-centered\">\n            <div class=\"modal-content\">\n              <div class=\"modal-header\">\n              <i class=\"bi bi-hand-thumbs-up fa-1x reaction-feedback\" style=\"width:48px;\"></i><h1 class=\"modal-title fs-5\" id=\"exampleModalLabel\">\n                &nbsp;\n                Why did you choose this rating?</h1>\n                <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"modal\" aria-label=\"Close\"></button>\n              </div>\n              <div class=\"modal-body\">\n              <textarea placeholder=\"Provide additional feedback\" class=\"userComment form-control\" id =\"userComment-").concat(messageID, "\"></textarea>\n              </div>\n              <div class=\"modal-footer\">\n                <button class=\"comment btn btn-primary btn-new-chat\" data-messageid=").concat(messageID, " data-user-comment-target=\".userComment\">Submit</button>                \n              </div>\n            </div>\n          </div>\n        </div>\n      ");
    chatHistory.appendChild(botMessage);
  }

  $(document).on('click', '.comment', function () {
    submitComment($(this));
  }); // Function to display a loading animation message in the chat interface

  function displayLoadingAnimation() {
    $("div.loading-animation").remove();
    var chatHistory = document.getElementById('chatbot-prompt');
    var botMessage = document.createElement('div');
    botMessage.classList.add('card', 'loading-animation');
    botMessage.innerHTML = "\n          <div class=\"card-body\">\n            <div class=\"row\">\n            <div class=\"col-xs-12 col-sm-12 col-md-2 col-lg-2 col-xl-2 col-2 d-flex flex-wrap align-items-center justify-content-center\">\n            <img class=\"waterdrop2\" />\n          </div>\n              <div class=\"col-md-10 align-items-center\" style=\"display:inline-flex;\">\n                    <div class=\"loader\"></div> &nbsp; <span class=\"text-primary\">Generating response...</span>\n              </div>\n            </div>\n        </div>\n      ";
    chatHistory.appendChild(botMessage); //Showing loading animation before the response

    $(".loading-animation").css("display", "flex");
  }

  function removeLoadingAnimation() {
    //Removing loading animation after the response
    $(".loading-animation").css("display", "none");
  } // Function to send user queries to the backend and receive responses


  function sendUserQuery(e) {
    var userQuery = document.getElementById('user_query').value;
    e.preventDefault();

    if (userQuery.trim() === '') {
      return; // Don't send empty queries
    } // Display the user's message in the chat


    displayUserMessage(userQuery);
    $('.followup-buttons').hide(); //Start of the loading animation

    displayLoadingAnimation();
    $("#user_query").prop('disabled', true);
    $("#submit-button").prop('disabled', true); //Scroll to bottom script

    scrollToBottom(); // Define the URL of your Flask server

    var apiUrl = "/chat_api"; // Replace with the actual URL if needed
    // Create a request body with the user query

    var requestBody = new FormData();
    requestBody.append('user_query', userQuery);
    fetch(apiUrl, {
      method: 'POST',
      body: requestBody
    }).then(function (response) {
      return response.json();
    }).then(function (botResponse) {
      // Display the bot's response in the chat
      //debugger;
      displayBotMessage(botResponse.resp, botResponse.msgID); //typewriter(botResponse);
      //Removing loading animation

      removeLoadingAnimation();
      $("#user_query").prop('disabled', false);
      $("#submit-button").prop('disabled', false); //Scroll to bottom function

      scrollToBottom();
    })["catch"](function (error) {
      console.error('Error:', error);
      removeLoadingAnimation();
      $("#user_query").prop('disabled', false);
      $("#submit-button").prop('disabled', false);
      scrollToBottom();
    });
    scrollToBottom(); // Clear the input field after sending the query

    document.getElementById('user_query').value = '';
  }

  $("#user_query").on('keyup', function (e) {
    e.preventDefault();

    if (e.key === 'Enter' || e.keyCode === 13) {
      sendUserQuery(e);
    }
  });
  $("#submit-button").on('click', function (e) {
    e.preventDefault();
    sendUserQuery(e);
  });
  $(document).on('mouseover', '.welcome-message', function () {
    showReactions($(this));
  });
  $(document).on('mouseout', '.welcome-message', function () {
    hideReactions($(this));
  }); // Bind click event to submit the reaction for all elements with the class 'reactions'

  $(document).on('click', '.reaction', function () {
    submitReaction($(this));
    var messageID = $(this).parent().parent().find("button.comment").attr("data-messageid");
    var reactionId = $(this).attr("data-reaction");
    $("#modal-" + messageID).find("button.comment").attr("data-reaction", reactionId);
  });
  $(document).on('click', '.followup-buttons', function () {
    var buttonId = $(this).attr('id');

    switch (buttonId) {
      case 'shortButton':
        callAPI('/chat_short_api');
        break;

      case 'detailedButton':
        callAPI('/chat_detailed_api');
        break;

      case 'actionItemsButton':
        callAPI('/chat_actionItems_api');
        break;

      case 'sourcesButton':
        callAPI('/chat_sources_api');
        break;
      // Add more cases for additional buttons if needed
    }
  });

  function callAPI(apiUrl) {
    console.log("Calling API: " + apiUrl);
    $('.followup-buttons').hide();
    displayLoadingAnimation();
    scrollToBottom();
    fetch(apiUrl, {
      method: 'POST'
    }).then(function (response) {
      return response.json();
    }).then(function (botResponse) {
      displayBotMessage(botResponse.resp, botResponse.msgID);
      removeLoadingAnimation();
      $("#user_query").prop('disabled', false);
      $("#submit-button").prop('disabled', false);
      scrollToBottom();
    })["catch"](function (error) {
      console.error('Error:', error);
      removeLoadingAnimation();
      $("#user_query").prop('disabled', false);
      $("#submit-button").prop('disabled', false);
      scrollToBottom();
    });
  }

  function scrollToBottom() {
    $("#chatbot-prompt").scrollTop($('#chatbot-prompt')[0].scrollHeight - $('#chatbot-prompt')[0].clientHeight);
  }
});
import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';

import { Accounts } from 'meteor/accounts-base';

import './main.html';

Accounts.ui.config({
    passwordSignupFields: 'USERNAME_ONLY'
});

Template.loginButtons.rendered = function(){
    Accounts._loginButtonsSession.set('dropdownVisible', true);
};

Template.outputZone.helpers({
    sorted: function() {
        var sorted_json = Session.get("sorted");
        var sorted = sorted_json ? sorted_json.sorted : null

        return sorted;
    }
});

Template.submitZone.events({
    'submit .new-numbers'(event) {
        // Prevent default browser form submit
        event.preventDefault();

        // Get value from form element
        const target = event.target;
        const text = target.numbers.value;
        if (Meteor.projectFunctions.valid_data(text)) {
            sAlert.success('Sorting in progress', {position: 'bottom', timeout: '3000'});

            // call server method to sort
            Meteor.call('sortNumbers', text, function(err, data){
                console.log(data);
                // update session in callback from server call
                Session.set("sorted", data);
            });
        }
        else {
            sAlert.error('Data inserted not valid', {position: 'bottom', timeout: '3000'});
            //alert("data inserted not valid");
        }
    }
});

Meteor.projectFunctions = {
    valid_data: function(data){
        // "-1" or "2.3,-2,2" => ^ (\-?\d*\.?\d*) (\, (\-?\d*\.?\d*))* $
        var re = /^(\-?\d*\.?\d*)?(\,\-?\d*\.?\d*)*$/
        var valid = data.match(re)
        return !!valid;
    }
};

Template.outputZone.onCreated(function(){
    // reset sorted data on startup
    Session.set("sorted", "");
});



















// Template.outputZone.onCreated(function helloOnCreated() {
//   // counter starts at 0
//   this.counter = new ReactiveVar(0);
//
// });

// Template.hello.helpers({
//   counter() {
//     return Template.instance().counter.get();
//   },
// });
//

// Template.hello.events({
//   'click button'(event, instance) {
//     // increment the counter when button is clicked
//     instance.counter.set(instance.counter.get() + 1);
//   },
// });
//

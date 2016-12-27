import { Meteor } from 'meteor/meteor';

Meteor.startup(() => {
    Meteor.methods({
		sortNumbers: function(data){  
            Meteor._sleepForMs(2000);
            var numbers = data.split(',').sort(function (a, b) {  return a - b;  });
            result = {
                sorted: numbers
            }
            console.log(result);
            return result;
        }
    });
});

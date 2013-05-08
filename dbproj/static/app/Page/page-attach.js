define(['zest', 'jquery'], function($z) {

  return $z.create([$z.Constructor, $z.InstanceEvents], {

    _events: ['logIn'],

    construct: function(el, o) {

      // Set references to Zest components
      this.$main = $('#main', el);
      this.list = $z.select('#main-list', el);
      this.studentno_input = $z.select('.studentno-input', el);
      this.password_input = $z.select('.password-input', el);
      this.login_btn = $z.select('.login-btn', el);

      // Set event functions
      this.login_btn.click.on(this.logIn);

      this.init();

    },

    prototype: {

      init: function() {
        this.unsetLoading();
      },

      setLoading: function() {
        this.$main.css('height', this.$main.outerHeight() );
        this.$main.addClass('loading');
      },

      unsetLoading: function() {
        this.$main.removeAttr('style');
        this.$main.removeClass('loading');
      },

      /** 
       * Process to log in and authenticate a user
       * Event which fires when the Log In button is pressed
       **/
      logIn: function(o) {

        // Gather the user credentials
        var self = this,
            user = this.studentno_input.getValue(),
            pass = $('#password').val(),
            pass_hash = CryptoJS.MD5(pass).toString();

          /**
           * Initiate the entire authentication process.
           * This entire process uses 'promises' to maintain an asynchronous process.
           * It's a myriad of callback functions flowing through .done and .fail callbacks...
           **/

          // ...First we submit the student number to the server and get the stored salt and temp_salt...
          self.post_json('get_salt', {'studentno': user} )
            .done( function(result) {
              // ... then we process the salts with the password and send that for authentication...
              self.process_salts( result, self.pass )

                .done( function(result) {
                  // .. then we handle the authentication result (true/false)
                  self.handle_authentication_status(result);
                })

                // handle any errors in submitting the salt hash.
                .fail( function(result) {
                  console.log('Error posting salted hash.');
                })
            })

            // handle any errors in submitting the student number
            .fail(function() {
              console.log('Error posting studentno.');
            });

            // preventDefault - we don't want the button to submit any forms.
            return false;

      },

      /**
       * Function to perform a generic $.ajax POST request to the flask server
       * It always sends and receives json data.
       * @param url, the trailing url string for the route, ignore http://localhost:port
       * @param data, the json data object to be posted
       * @param proceed, the callback function which will be called when the server responds the post
       **/
      post_json: function(url, json_data) {
        return $.ajax({
          type: 'POST',
          url: 'http://localhost:5000/' + url,
          data: JSON.stringify( json_data ),
          contentType:"application/json; charset=utf-8",
          dataType: 'json'
        });
      },   

      /**
       * Function used to process the salts which is returned by the server,
       * It generates the final hash string which is used for authentication
       * @param data, the json object with the salt and temp_salt strings
       **/
      process_salts: function(json_data, pass) {

        var studentno = json_data.studentno,
            salt = json_data.salt,
            temp_salt = json_data.temp_salt,
            md5 = CryptoJS.MD5;

        // Hash the password, salt and temp salt to form the final hash string
        var hashed_string =  md5( ( md5(pass).toString() + salt ).toString() + md5(temp_salt).toString() ).toString();

        // Send the hashed string back to the server along with the username, final authentication step
        return this.post_json('login', {'studentno': studentno, 'hash': hashed_string});

      },

      /**
       * Function which handles what happens when we get our authentication status back
       * @param data, the {authentication: true/false} json object
       **/
      handle_authentication_status: function(authentication) {

        if(authentication.status == 'true') {
          var self = this;
          this.setLoading();
          $.when( this.list.clearList() ).done(function() {
            self.displayMenu();
          });
        }
      },

      /**
       * PAGE DISPLAYS
       */

      displayMenu: function(o) {
        var self = this;
        $z.render('Draw the main menu or something else', document.querySelector('#list-container'), function() {
          console.log('menu displayed');
          self.unsetLoading();  
        });
      },

      dispose: function() {}

    }

  });

});
$(document).ready(function() {

  // Parse JSON
  $.getJSON('/files/main.json', function(json_main) {
    // Build ul.selector-family
    var itens = '';
    $.each(json_main, function(control_class, families) {
      itens += '<li id="' + control_class + '" class="item-control-class">' + control_class + '<ul>';
      $.each(families, function(family, numbers) {
        itens += '<li id="' + family + '" class="item-family clickable">' + family + '</li>';
      });
      itens += '</ul></li>';
    });
    $('ul.selector-family').html(itens);

    // Click event to build ul.selector-number
    $('ul.selector-family').on('click', 'li.item-family', function() {
      // Clear previous content
      $('h2.title-content').html('');
      $('div.text-content').html('');
      var control_class = $(this).closest('li.item-control-class').prop('id'),
          family = $(this).prop('id'),
          itens = '';
      $('h2.title-family').html(control_class + ' - ' + family);
      $.each(json_main[control_class][family], function(number, value) {
        itens += '<li id="' + number + '" class="item-number clickable">' + number + ' - ' + value.title + ( value.priority ? (' - ' + value.priority ) : '' ) + '</li>';
      });
      $('ul.selector-number').html(itens);
    });
  });

  function xhtml_parser(key, value) {
   // Parse JSON to HTML
   var content = '';
   switch(key) {
     case 'ns2:p':
       content = value['#text'];
       if (value['ns2:em']) content = content.replace('[]', '[' + value['ns2:em'] + ']');
       break;
     case 'ns2:ol':
       content = '<ol>';
       for (var i = 0; i < value['ns2:li'].length; i++) {
         if ( typeof value['ns2:li'][i] !== 'string' ) {
           var holder = '<li>' + value['ns2:li'][i]['#text'] + '</li>';
           if ( typeof value['ns2:li'][i]['ns2:em'] !== 'string' ) {
             for (var j = 0; j < value['ns2:li'][i]['ns2:em'].length; j++) {
               holder = holder.replace('[]', '[' + value['ns2:li'][i]['ns2:em'][j] + ']');
             }
           }
           else holder = holder.replace('[]', '[' + value['ns2:li'][i]['ns2:em'] + ']');
           content += holder;
         }
         else content += '<li>' + value['ns2:li'][i] + '</li>';
       }
       content += '</ol>';
       break;
     default:
       content = '{ERROR} couldn\'t parse key: [' + key + ']';
       break;
   }
   return content;
  }

  $('ul.selector-number').on('click', 'li.item-number', function() {
    $('h2.title-content').html('Loading, please wait...');
    $('div.text-content').html('');
    var title = $(this).html(),
        number = $(this).prop('id');
    $.getJSON('/files/nist/' + number + '.json', function(json_data) {
      $('h2.title-content').html(title);
      $('div.text-content').html('<a href="#" id="' + number + '" class="btn btn-primary btn-add float-right">Add</a>');
      if (json_data['description']) {
        $('div.text-content').append('<h3>Description</h3>');
        $.each(json_data['description']['ns2:div'], function(key, value) {
          $('div.text-content').append( xhtml_parser(key, value) );
        });
      }
      if (json_data['supplemental_guidance']) {
        $('div.text-content').append('<h3>Supplemental Guidance</h3>');
        $.each(json_data['supplemental_guidance']['ns2:div'], function(key, value) {
          $('div.text-content').append( xhtml_parser(key, value) );
        });
      }
      if (json_data['references']) {
        $('div.text-content').append('<h3>References</h3>');
        if (Array.isArray(json_data['references'])) {
          $.each(json_data['references'], function(key, value) {
            $('div.text-content').append('<a href="' + value['@href'] + '" target="_blank">' + value['#text'] + '</a><br>');
          });
        }
        else $('div.text-content').append('<a href="' + json_data['references']['@href'] + '" target="_blank">' + json_data['references']['#text'] + '</a><br>');
      }
      if (json_data['control_enhancements']) {
        var content = '<h3>Control Enhancements</h3>';
        if (Array.isArray(json_data['control_enhancements'])) {
          content += '<ol>';
          $.each(json_data['control_enhancements'], function(k, jce) {
            content += '<li>';
            if (jce['description']) {
              content += '<p><b>Description: </b>';
              $.each(jce['description']['ns2:div'], function(key, value) {
                content += xhtml_parser(key, value);
              });
              content += '</p>';
            }
            if (jce['supplemental-guidance']) {
              content += '<p><b>Supplemental Guidance: </b>';
              $.each(jce['supplemental-guidance']['ns2:div'], function(key, value) {
                content += xhtml_parser(key, value);
              });
              content += '</p>';
            }
            content += '</li><hr>';
          });
          content += '</ol>';
        }
        else {
          if (json_data['control_enhancements']['description']) {
            content += '<p><b>Description: </b>';
            $.each(json_data['control_enhancements']['description']['ns2:div'], function(key, value) {
              content += xhtml_parser(key, value);
            });
            content += '</p>';
          }
          if (json_data['control_enhancements']['supplemental-guidance']) {
            content += '<p><b>Supplemental Guidance: </b>';
            $.each(json_data['control_enhancements']['supplemental-guidance']['ns2:div'], function(key, value) {
              content += xhtml_parser(key, value);
            });
            content += '</p>';
          }
        }
        $('div.text-content').append(content);
      }
    });
  });

  // Itens selector
  var list_build = {};

  $('div.text-content').on('click', 'a.btn-add', function() {
    var number = $(this).prop('id');
    list_build[number] = $('h2.title-content').html();
    $('ul.list-number').html('');
    $.each(list_build, function(key, value) {
      $('ul.list-number').append('<li id="' + key + '">' + value + '</li>');
    });
  });

  $('a.btn-clear').click(function() {
    list_build = {};
    $('ul.list-number').html('');
  });

  $('a.btn-print').click(function() {
    list = JSON.stringify(list_build);
    console.log('requesting ', list);
    $.post(window.location, {listing: list}, function(data) {
      console.log('calling');
    })
    .done(function(data) {
      console.log('success');
      $('a#btn-download').prop('href', data);
      document.getElementById('btn-download').click();
    })
    .fail(function() {
      window.alert('Houve um erro ao trazer o arquivo para o navegador, por favor vá até o diretório padrão para obtê-lo.');
    });
  });

});

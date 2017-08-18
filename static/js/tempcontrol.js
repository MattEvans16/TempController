    function pollTemp()
    {
        $.post('/get/temp',function(data)
        {
            console.log("recv /get/temp: " + JSON.stringify(data));
            
            if ('tempF' in data)
                $('#currentTemp').html(data['tempF'])
            if ('humidity' in data)
                $('#currentHumidity').html(data['humidity'])
        });
        
        setTimeout(pollTemp.bind(null),1000);
    }
    
    
$(document).ready(function() {

    $(function() {
        $('#toggle-power').change(function() {
          console.log('Toggle: ' + $(this).prop('checked'))
          $.post('set/power', {powerValue: $(this).prop('checked') ? 1 : 0}, function(data)
          {
            console.log("recv set/power/ back. " + JSON.stringify(data));
          });
        })
      })
    
  pollTemp();

})
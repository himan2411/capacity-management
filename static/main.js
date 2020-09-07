function myFunction() {
    var x = document.getElementsByName("requestor_serviceline");
    if(x.length >0)
    {
        if(x[0].value == "serviceline1")
        {
            document.getElementById("myRange_1").value = 30
            document.getElementById("myRange_2").value = 10
            document.getElementById("myRange_7").value = 10
            document.getElementById("myRange_3").value = 0
            document.getElementById("myRange_4").value = 10
            document.getElementById("myRange_5").value = 30
            document.getElementById("myRange_6").value = 10
        }
        if(x[0].value == "serviceline2")
        {
            document.getElementById("myRange_1").value = 40
            document.getElementById("myRange_2").value = 10
            document.getElementById("myRange_7").value = 10
            document.getElementById("myRange_3").value = 0
            document.getElementById("myRange_4").value = 10
            document.getElementById("myRange_5").value = 25
            document.getElementById("myRange_6").value = 5
        }
        if(x[0].value == "serviceline3")
        {
            document.getElementById("myRange_1").value = 10
            document.getElementById("myRange_2").value = 20
            document.getElementById("myRange_7").value = 0
            document.getElementById("myRange_3").value = 30
            document.getElementById("myRange_4").value = 15
            document.getElementById("myRange_5").value = 20
            document.getElementById("myRange_6").value = 5
        }
    }
  }   

  function checkSum() {
    var sum = +(document.getElementById("myRange_1").value) + +(document.getElementById("myRange_2").value) +
     +(document.getElementById("myRange_3").value) + +(document.getElementById("myRange_4").value) +
     +(document.getElementById("myRange_5").value) + +(document.getElementById("myRange_6").value) + +(document.getElementById("myRange_7").value);
     
     if( sum != 100){
        document.getElementById("submit_btn").disabled = true;
     }
     else{
        document.getElementById("submit_btn").disabled = false;
     }
}
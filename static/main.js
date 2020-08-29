function myFunction() {
    var x = document.getElementsByName("requestor_serviceline");
    if(x.length >0)
    {
        if(x[0].value == "ServiceLine1")
        {
            document.getElementById("myRange_1").value = 30
            document.getElementById("myRange_2").value = 10
            document.getElementById("myRange_7").value = 10
            document.getElementById("myRange_3").value = 0
            document.getElementById("myRange_4").value = 10
            document.getElementById("myRange_5").value = 30
            document.getElementById("myRange_6").value = 10
        }
        if(x[0].value == "ServiceLine2")
        {
            document.getElementById("myRange_1").value = 40
            document.getElementById("myRange_2").value = 10
            document.getElementById("myRange_7").value = 10
            document.getElementById("myRange_3").value = 0
            document.getElementById("myRange_4").value = 10
            document.getElementById("myRange_5").value = 25
            document.getElementById("myRange_6").value = 5
        }
        if(x[0].value == "ServiceLine3")
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
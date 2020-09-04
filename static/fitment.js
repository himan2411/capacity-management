function change_dispaly() 
{
    var x = document.getElementById("fitment_dropdown");
    if(x.value == "all")
    {
        var table = document.getElementsByClassName("emp_table")[0];
        for (var i = 0, row; row = table.rows[i]; i++) {
            //iterate through rows
            //rows would be accessed using the "row" variable assigned in the for loop
            row.style.display = 'block';
        }
    }
    if(x.value == "best_fit")
    {
        var table = document.getElementsByClassName("emp_table")[0];
        for (var i = 0, row; row = table.rows[i]; i++) {
            //iterate through rows
            //rows would be accessed using the "row" variable assigned in the for loop
            if(+(row.cells[2].textContent) < 85)
            {
                row.style.display = 'none';
            }
            else{
                row.style.display = 'block';
            }
        }
    }
    if(x.value == "stretched_fit")
    {
        var table = document.getElementsByClassName("emp_table")[0];
        for (var i = 0, row; row = table.rows[i]; i++) {
            //iterate through rows
            //rows would be accessed using the "row" variable assigned in the for loop
            if(+(row.cells[2].textContent) < 70 ||+(row.cells[2].textContent) >85)
            {
                row.style.display = 'none';
            }
            else{
                row.style.display = 'block';
            }    
        }
    }
    if(x.value == "best_bet")
    {
        var table = document.getElementsByClassName("emp_table")[0];
        for (var i = 0, row; row = table.rows[i]; i++) {
            //iterate through rows
            //rows would be accessed using the "row" variable assigned in the for loop
            if(+(row.cells[2].textContent) < 60 ||+(row.cells[2].textContent) >70)
            {
                row.style.display = 'none';
            }
            else{
                row.style.display = 'block';
            }
        }
    }
}
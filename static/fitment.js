function change_dispaly() 
{
    console.log("called")
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

function sort_by_percentage()
{
    console.log("sort_by_percentage")

    var sorted_table = document.getElementsByClassName("sorting_by_percentage")[0];
    var table = document.getElementsByClassName("sorting_by_both")[0];
    var chbox = document.getElementById("percentage")

    if(chbox.checked)
    {
        console.log("in if")
        
        sorted_table.style.display = 'block';
        table.style.display = 'none';
    }
    else{
        sorted_table.style.display = 'none';
        table.style.display = 'block';
    }
}
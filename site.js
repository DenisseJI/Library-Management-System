$(document).ready(function() {
    //API url of Google Books
    var bookUrl = "https://www.googleapis.com/books/v1/volumes?q="
    //For books that do not come with a cover image
    var placeHolder = '<img src="http://via.placeholder.com/640x360>'
    var data1;

    //Display Books In Library Page
    function InLibrary(){
      var element = document.getElementById("output1");
      if(typeof(element) != "undefined" && element != null){
        loadInBooksFromServer();
      }

    }
    InLibrary();
    //Retrieve and Display to html
    function loadInBooksFromServer(){

      output1.innerHTML = ""
      fetch("http://localhost:8080/book").then(function(response){
        response.json().then(function (dataFromServer){
         
            books = dataFromServer
            books.forEach(function (book){
              var title = book[1];
              var author = book[2];
              var publisher = book[4];
              var bookIsbn = book[3];
              var bookImg = book[5];
      
              var column = document.createElement("div");
              column.setAttribute("class", "column");

              var book = document.createElement("div");
              book.setAttribute("class", "thebook");
              var imageDiv = document.createElement("div");
              imageDiv.innerHTML = `<img src="${bookImg}" class="card-img" alt="...">`;
              book.appendChild(imageDiv);
      
              var titleH5 = document.createElement("h5");
              titleH5.innerHTML = 'Title: ' + title;
              book.appendChild(titleH5);
      
              var authorP = document.createElement("p");
              authorP.innerHTML = 'Author: ' + author;
              book.appendChild(authorP);
      
              var publisherP = document.createElement("p");
              publisherP.innerHTML = 'Publisher: ' + publisher;
              book.appendChild(publisherP);
      
              var checkoutButton = document.createElement("button");
              checkoutButton.setAttribute("class", "add-library");
              checkoutButton.innerHTML = "Checkout Book";
              checkoutButton.onclick = function (){
                checkOutBook(title, author, bookIsbn, publisher, bookImg)
              }

              book.appendChild(checkoutButton);
              column.appendChild(book);
              output1.appendChild(column);
      
      
             
            })

        })
      })

    }

    //Display Books Checked Out Page
    function InCheckedOut(){
      var element = document.getElementById("output2");
      if(typeof(element) != "undefined" && element != null){
        loadOutBooksFromServer();
      }
    }
    InCheckedOut();
    
    //Retrieve and Display to html
    function loadOutBooksFromServer(){
      output2.innerHTML = ""
      fetch("http://localhost:8080/bookout").then(function(response){
        response.json().then(function (dataFromServer){
        
          books = dataFromServer
            books.forEach(function (book){
              var title = book[1];
              var author = book[2];
              var publisher = book[4];
              var bookIsbn = book[3];
              var bookImg = book[5];
      
              var column = document.createElement("div");
              column.setAttribute("class", "column");

              var book = document.createElement("div");
              book.setAttribute("class", "thebook");
              var imageDiv = document.createElement("div");
              imageDiv.innerHTML = `<img src="${bookImg}" class="card-img" alt="...">`;
              book.appendChild(imageDiv);
      
              var titleH5 = document.createElement("h5");
              titleH5.innerHTML = 'Title: ' + title;
              book.appendChild(titleH5);
      
              var authorP = document.createElement("p");
              authorP.innerHTML = 'Author: ' + author;
              book.appendChild(authorP);
      
              var publisherP = document.createElement("p");
              publisherP.innerHTML = 'Publisher: ' + publisher;
              book.appendChild(publisherP);
      
              var checkinButton = document.createElement("button");
              checkinButton.setAttribute("class", "add-library");
              checkinButton.innerHTML = "Check Book In";
              checkinButton.onclick = function (){
                checkInBook(title, author, bookIsbn, publisher, bookImg)
              }
              
              book.appendChild(checkinButton);
              column.appendChild(book);

      
              output2.appendChild(column);
      
             
            })
        })
      })

    }

    //search button, Retrieve searched book from Google Books API
    $("#search-button").click(function() {
        output.innerHTML = ""
        //gets value from the user input (search bar)
        data1 = $("#search-bar").val();
        //if there is not search, nothing was entered
        if(data1 === "" || data1 === null){
            displayError();
        }
        else{
            $.ajax({
                url: bookUrl + data1,
                dataType: "json", 
                success: function(response){
                    //show the response from the request in the log
                    console.log(response)
                    if(response.totalItems === 0){
                        alert("There are no results from your search");
                    }
                    else{
                        $("#title").animate({'margin-top': '10px'}, 1000);
                        $(".book-list").css("visibility", "visible");
                        displayResults(response);


                    }
                },
                error : function() {
                    alert("There was something wrong :( ");
                }
            });
        }
        //clear the search bar
        $("#search-bar").val("");

    });


    //display results in search.html
    //books retrieved from the Google Books API
    function displayResults(response) {
      books = response.items;
      books.forEach(function (book){
        var title = book.volumeInfo.title;
        var author = book.volumeInfo.authors;
        var publisher = book.volumeInfo.publisher;
        var bookIsbn = book.volumeInfo.industryIdentifiers[1].identifier
        var bookImg = (book.volumeInfo.imageLinks) ? book.volumeInfo.imageLinks.thumbnail : placeHolder;

        

        var column = document.createElement("div");
        column.setAttribute("class", "column");
      

        var book = document.createElement("div");
        book.setAttribute("class", "thebook");
        var imageDiv = document.createElement("div");
        imageDiv.innerHTML = `<img src="${bookImg}" class="card-img" alt="...">`;
        book.appendChild(imageDiv);

        var titleH5 = document.createElement("h5");
        titleH5.innerHTML = 'Title: ' + title;
        book.appendChild(titleH5);

        var authorP = document.createElement("p");
        authorP.innerHTML = 'Author: ' + author;
        book.appendChild(authorP);

        var publisherP = document.createElement("p");
        publisherP.innerHTML = 'Publisher: ' + publisher;
        book.appendChild(publisherP);

        var addButton = document.createElement("button");
        addButton.setAttribute("class", "add-library");
        addButton.innerHTML = "Add Book to Library";
        addButton.onclick = function (){
          addBook(title, author, bookIsbn, publisher, bookImg);
        }
        
        book.appendChild(addButton);

        column.appendChild(book);

        output.appendChild(column);
       
      })
                
    }

    //Google API to Local Server API
    //pass to python, local server API to add to library SQLite database IN table
    function addBook(title, author, isbn, publisher, img){
      var data = "title=" + encodeURIComponent(title) + "&author=" + encodeURIComponent(author) + "&isbn=" + encodeURIComponent(isbn) + "&publisher=" + encodeURIComponent(publisher) + "&img=" + encodeURIComponent(img)

      fetch("http://localhost:8080/book", {
        method: "POST",
        body: data,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
      } 
    }).then(function(response){
      if(response.ok){
        return response.json();
      }else{
        console.log("Error")
      }
      return Promise.reject(response);
    }).then(function (data) {
      console.log(data);
    })
  }

  //from IN table to OUT table
  //pass to python, local server API to add to library SQLite database OUT table
  function checkOutBook(title, author, isbn, publisher, img){
    var data = "title=" + encodeURIComponent(title) + "&author=" + encodeURIComponent(author) + "&isbn=" + encodeURIComponent(isbn) + "&publisher=" + encodeURIComponent(publisher) + "&img=" + encodeURIComponent(img)

    fetch("http://localhost:8080/bookout", {
      method: "POST",
      body: data,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
    } 
  }).then(function(response){
    if(response.ok){
      return response.json();
    }else{
      console.log("Error")
    }
    return Promise.reject(response);
  }).then(function (data) {
    console.log(data);
  })
}

//from OUT table to IN table
  //pass to python, local server API to add to library SQLite database IN table
function checkInBook(title, author, isbn, publisher, img){
  var data = "title=" + encodeURIComponent(title) + "&author=" + encodeURIComponent(author) + "&isbn=" + encodeURIComponent(isbn) + "&publisher=" + encodeURIComponent(publisher) + "&img=" + encodeURIComponent(img)

  fetch("http://localhost:8080/bookin", {
    method: "POST",
    body: data,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
  } 
}).then(function(response){
  if(response.ok){
    return response.json();
  }else{
    console.log("Error")
  }
  return Promise.reject(response);
}).then(function (data) {
  console.log(data);
})
}
    
    
})



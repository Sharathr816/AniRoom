
//mock search
const aniRepoItems = [
  { id: 1, title: "Vivy: Fluorite Eye's Song", type: "anime" },
  { id: 2, title: "Power Jump", type: "clip" },
  { id: 3, title: "Roshidere", type: "anime" },
  { id: 4, title: "Angel Next Door", type: "image" }
];

//search bar event listener
document.addEventListener('DOMContentLoaded', SearchBarFun);

function SearchBarFun() {
  //get elements
  const searchLink = document.getElementById('search-link');
  const searchContainer = document.getElementById('search-container');
  const searchBar = document.getElementById('search-bar');

    //check if no elements are null
  if (searchLink && searchContainer && searchBar) {
    //when the search link is clicked
    searchLink.addEventListener('click', function (e) {
      searchContainer.style.display = 'block';
      searchBar.focus();
    });

    //when enter key is pressed in search bar
    searchBar.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        const query = searchBar.value.trim().toLowerCase();
        const found = aniRepoItems.find(item => item.title.toLowerCase().includes(query));
        if (found) {
          const resultWindow = window.open('', '_blank');
          resultWindow.document.write(`
            <h1>${found.title}</h1>
            <p>Type: ${found.type}</p>
          `);
        }
        else {
          alert('No result found.');
        }
      }
    });

  }
   //if an element is null
   else {
    console.error("Search elements not found.");
  }
}




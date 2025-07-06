

//search bar event listener
document.addEventListener('DOMContentLoaded', SearchBarFun);

function SearchBarFun() {
  //get elements
  const searchLink = document.getElementById('search-link');
  const searchContainer = document.getElementById('search-container');
  const searchBar = document.getElementById('search-bar');
  const form = document.getElementById('search-form');

    //check if no elements are null
  if (searchLink && searchContainer && searchBar) {
    //when the search link is clicked
    searchLink.addEventListener('click', function (e) {
      searchContainer.style.display = 'block';
      searchBar.focus();
    });
  }
   //if an element is null
   else {
    console.error("Search elements not found.");
  }
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('search-form');
    const input = document.getElementById('search-bar');
           // Initialize all carousels
    const carousels = document.querySelectorAll('.Carousel');

    form.addEventListener('submit', function (e) {
//        e.preventDefault(); // Stop normal form submit
        const query = input.value.trim();

        // If query is not empty, redirect to ?q=...
        if (query) {
            window.location.href = `?q=${encodeURIComponent(query)}`;
        }
    });

    // Optional: Auto-reset query param on refresh
    if (window.location.search.includes('?q=')) {
        if (performance.navigation.type === performance.navigation.TYPE_RELOAD) {
            window.location.href = window.location.pathname; // Strip ?q=...
        }
    }



    carousels.forEach(carousel => {
        // Create navigation buttons
        const prevButton = document.createElement('button');
        prevButton.className = 'carousel-nav prev';
        prevButton.innerHTML = '';
        const nextButton = document.createElement('button');
        nextButton.className = 'carousel-nav next';
        nextButton.innerHTML = '';

        // Append buttons to carousel container
        carousel.parentNode.insertBefore(prevButton, carousel);
        carousel.parentNode.appendChild(nextButton);

        // Scroll functionality
        const items = carousel.querySelectorAll('.img-box');
        let scrollAmount = 0;
        const itemWidth = items[0].offsetWidth + 16; // Including gap

        prevButton.addEventListener('click', () => {
            scrollAmount = Math.max(scrollAmount - itemWidth * 3, 0);
            carousel.scrollTo({ left: scrollAmount, behavior: 'smooth' });
        });

        nextButton.addEventListener('click', () => {
            const maxScroll = carousel.scrollWidth - carousel.clientWidth;
            scrollAmount = Math.min(scrollAmount + itemWidth * 3, maxScroll);
            carousel.scrollTo({ left: scrollAmount, behavior: 'smooth' });
        });

        // Touch support
        let startX = 0;
        let scrollStart = 0;

        carousel.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            scrollStart = carousel.scrollLeft;
        });

        carousel.addEventListener('touchmove', (e) => {
            const deltaX = startX - e.touches[0].clientX;
            carousel.scrollLeft = scrollStart + deltaX;
        });

        carousel.addEventListener('touchend', () => {
            // Snap to nearest item
            scrollAmount = Math.round(carousel.scrollLeft / itemWidth) * itemWidth;
            carousel.scrollTo({ left: scrollAmount, behavior: 'smooth' });
        });
    });
});





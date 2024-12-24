document.addEventListener("DOMContentLoaded", () => {
    const searchBox = document.getElementById("search-box");
    const booksContainer = document.getElementById("books-container");
    const favoritesContainer = document.getElementById("favorites-container");

    searchBox.addEventListener("input", (e) => {
        const query = e.target.value.toLowerCase();
        
        const filterItems = (container, itemClass) => {
            const items = container.querySelectorAll(`.${itemClass}`);
            items.forEach((item) => {
                const title = item.getAttribute("data-title");
                const author = item.getAttribute("data-author");
                if (title.includes(query) || author.includes(query)) {
                    item.style.display = "";
                } else {
                    item.style.display = "none";
                }
            });
        };

        if (booksContainer) filterItems(booksContainer, "book-item");
        if (favoritesContainer) filterItems(favoritesContainer, "favorite-item");
    });
});

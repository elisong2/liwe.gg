"use client";

import React from "react";

// =================== Search.tsx ===================

import { useState } from "react";

// ① Define props type: we expect the parent to give us ONE thing:
//    a function called onSearch that accepts a string and returns nothing.
type SearchProps = {
  onSearch: (query: string) => void; // <-- pipeline to parent
};

// ② This is the Search component itself
export function Searchbar({ onSearch }: SearchProps) {
  // ③ Internal state for what's currently typed in the search bar
  const [value, setValue] = useState("");

  // ④ Function to actually "send" the search to parent
  const triggerSearch = () => {
    if (value.trim() !== "") {
      console.log("User searched for:", value);
      onSearch(value.trim()); // <-- give current text to parent
      setValue(""); // <-- clear the search bar after sending
    }
  };

  // ⑤ Function for when the user types
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value); // <-- keep `value` updated with what’s typed
  };

  // ⑥ Function for when a key is pressed (like Enter)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      // <-- only trigger search on Enter key
      triggerSearch();
    }
  };

  // ⑦ What this component shows when rendered
  return (
    <input
      type="text"
      placeholder="Enter summoner#tag" // <-- hint for the user
      value={value} // <-- always reflect state
      onChange={handleChange} // <-- updates `value` on typing
      onKeyDown={handleKeyDown} // <-- checks for Enter
    />
  );
}

// export function Search() {
//   const searchBackend = (query: string) => {
//     console.log("Searching backend for:", query);
//   };

//   return (
//     <div>
//       <h1>Player Search</h1>
//       <Searchbar onSearch={searchBackend} />
//     </div>
//   );
// }

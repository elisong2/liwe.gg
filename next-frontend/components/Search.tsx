"use client";

import React, { useEffect, useRef, useState } from "react";
import { Field } from "@/components/ui/field";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";
import { Clock, SearchIcon, X } from "lucide-react";

// =================== Search.tsx ===================

// ① localStorage key and max number of recent searches to store
const STORAGE_KEY = "recent-summoners";
const MAX_RECENT = 5;

// ② Read the current list of recent searches from localStorage
//    Returns an empty array if we're on the server (SSR guard) or nothing is stored yet
const getRecent = (): string[] => {
  if (typeof window === "undefined") return [];
  return JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "[]");
};

// ③ Add a new search to the top of the recents list
//    - Removes duplicates (so re-searching moves it to the top instead of doubling up)
//    - Caps the list at MAX_RECENT entries
const addRecent = (name: string) => {
  const prev = getRecent();
  const updated = [name, ...prev.filter((n) => n !== name)].slice(
    0,
    MAX_RECENT,
  );
  localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
};

// ④ Remove a specific entry from the recents list
const removeRecent = (name: string) => {
  const updated = getRecent().filter((n) => n !== name);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
};

// ⑤ Props type: parent passes in a callback to receive the searched query
type SearchProps = {
  onSearch: (query: string) => void;
};

export function Searchbar({ onSearch }: SearchProps) {
  const [value, setValue] = useState(""); // what's currently typed
  const [recents, setRecents] = useState<string[]>([]); // recent searches to show in dropdown
  const [showDropdown, setShowDropdown] = useState(false); // whether the dropdown is visible
  const containerRef = useRef<HTMLDivElement>(null); // ref for detecting outside clicks

  // ⑥ If the user has typed something, narrow the dropdown to matching entries.
  //    Otherwise show all recents.
  const filtered = value.trim()
    ? recents.filter((n) => n.toLowerCase().startsWith(value.toLowerCase()))
    : recents;

  // ⑦ Core search handler — used by both Enter key and clicking a recent item
  //    Defaults to whatever is currently typed, but accepts an override (e.g. a clicked recent)
  const triggerSearch = (query: string = value) => {
    const trimmed = query.trim();
    if (!trimmed) return;
    addRecent(trimmed); // persist to localStorage
    setRecents(getRecent()); // sync state so dropdown reflects the new entry
    setShowDropdown(false); // close the dropdown
    onSearch(trimmed); // hand the query up to the parent
    setValue(""); // clear the input
  };

  // ⑧ Keep `value` in sync as the user types
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value);
  };

  // ⑨ Trigger search on Enter key
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") triggerSearch();
  };

  // ⑩ When the input is focused, load recents from localStorage and show the dropdown
  const handleFocus = () => {
    setRecents(getRecent());
    setShowDropdown(true);
  };

  // ⑪ Remove an individual entry and immediately re-sync state so the dropdown updates
  const handleRemove = (name: string) => {
    removeRecent(name);
    setRecents(getRecent());
  };

  // ⑫ Close the dropdown when the user clicks anywhere outside the component.
  //    We use mousedown (not click) so it fires before focus events and feels snappy.
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setShowDropdown(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler); // cleanup on unmount
  }, []);

  return (
    // ⑬ Wrapper div serves two purposes:
    //    - `relative` anchors the absolutely-positioned dropdown below the input
    //    - `containerRef` lets the outside-click handler know what's "inside" the component
    <div ref={containerRef} className="relative w-86">
      <Field>
        <InputGroup>
          <InputGroupInput
            type="text"
            id="inline-start-input"
            placeholder="OPMAGEMASTER#NA1"
            value={value}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            onFocus={handleFocus} // ← opens the dropdown
          />
          <InputGroupAddon align="inline-end">
            <SearchIcon className="text-muted-foreground" />
          </InputGroupAddon>
        </InputGroup>
      </Field>

      {/* ⑭ Dropdown — only renders if it's open and there are matching entries */}
      {showDropdown && filtered.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-background border border-border rounded-md shadow-lg z-50">
          <p className="text-xs text-muted-foreground px-3 pt-2 pb-1 uppercase tracking-widest">
            Recent
          </p>
          {filtered.map((name) => (
            <div
              key={name}
              className="flex items-center justify-between px-3 py-2 hover:bg-accent group"
            >
              {/* ⑮ Clicking the name fills + submits the search.
                      onMouseDown instead of onClick so it fires before the input's onBlur,
                      preventing the dropdown from vanishing before the click registers. */}
              <button
                className="flex items-center gap-2 text-sm flex-1 text-left"
                onMouseDown={() => triggerSearch(name)}
              >
                <Clock className="w-3 h-3 text-muted-foreground" />
                {name}
              </button>

              {/* ⑯ ✕ button to remove this entry. Hidden until the row is hovered (group-hover).
                      Also uses onMouseDown for the same reason as above. */}
              <button
                className="opacity-0 group-hover:opacity-100 transition-opacity"
                onMouseDown={() => handleRemove(name)}
              >
                <X className="w-3 h-3 text-muted-foreground hover:text-foreground" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

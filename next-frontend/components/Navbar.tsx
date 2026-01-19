import React from "react";
import Link from "next/link";

const Navbar = () => {
  return (
    <nav className="flex items-center gap-6 p-4">
      <ul>
        <li>
          <Link href="/" target="_self">
            Home
          </Link>
        </li>

        <li>
          <Link href="/about" target="_self">
            About
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;

// https://www.jegs.com/tech-articles/the-10-best-tuner-cars-to-modify/?srsltid=AfmBOopCG-HsPNWZykKPjsh1pdPSmTdoUU70Efm4I8k84I730JsXPVEr

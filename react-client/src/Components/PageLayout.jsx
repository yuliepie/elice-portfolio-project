import Navigation from "./Navigation";
import styled from "styled-components";

export default function PageLayout({ children }) {
  return (
    <div className="h-screen flex flex-col">
      <header>
        <Navigation />
      </header>
      <main className="pt-20 bg-indigo-50 bg-opacity-90 h-auto flex-grow">
        {children}
      </main>
      <footer className="mt-auto p-2.5 bg-red-300 text-center text-xs text-gray-800 z-20">
        Created by Yulie Jung.
      </footer>
    </div>
  );
}

import Navigation from "./Navigation";
import styled from "styled-components";

export default function PageLayout({ children }) {
  return (
    <div>
      <header>
        <Navigation />
      </header>
      <main className="pt-16 bg-pink-200 h-screen">{children}</main>
      <footer>Footer.</footer>
    </div>
  );
}

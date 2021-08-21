import { NavLink } from "react-router-dom";
import styled from "styled-components";

export default function Navigation() {
  return (
    <div className="border-2 border-red-500 h-16 bg-gray-500 flex justify-end px-8 py-2 items-center fixed w-full">
      <div className="border-2 border-blue-500 h-8 w-20">logo</div>
      <div className="inline-flex ml-auto gap-x-4">
        <div className="w-20 border-yellow-100 border-2">
          <NavLink to="/">네트워크</NavLink>
        </div>
        <div className="w-20 border-yellow-100 border-2">
          <NavLink to="/">마이페이지</NavLink>
        </div>
        <div className="w-20 border-yellow-100 border-2">
          <NavLink to="/">로그아웃</NavLink>
        </div>
      </div>
    </div>
  );
}

import PageLayout from "../../Components/PageLayout";
import { useAuth } from "../../Contexts/authContext";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import UserCard from "./UserCard";

export default function MainPage() {
  const [users, setUsers] = useState(null);
  const [query, setQuery] = useState("");

  // API Fetch
  async function fetchAllUsers() {
    try {
      const response = await axios.get("/api/users");
      setUsers(response.data.users);
    } catch (e) {
      console.log("Error in fetching users.");
    }
  }
  useEffect(() => {
    fetchAllUsers();
  }, []);

  async function fetchQueriedUsers() {
    try {
      const response = await axios.get(`/api/users?name=${query}`);
      setUsers(response.data.users);
    } catch (e) {
      console.log("Error in fetching users.");
    }
  }

  return (
    <PageLayout>
      <div className="bg-indigo-500 bg-opacity-80 w-full h-80 flex flex-col gap-8 items-center justify-center">
        <div className="header-text">Find your next connection.</div>
        <div className="w-1/3 pl-6 py-1 pr-1 rounded-full bg-white inline-flex justify-end shadow-lg">
          <input
            name="searchbox"
            type="text"
            className="focus:ring-transparent p-2 text-sm transparent border-none flex-1"
            placeholder="프로필을 검색해보세요!"
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={fetchQueriedUsers} className="main-btn w-20">
            검색
          </button>
        </div>
      </div>
      <div className="px-20 py-10 overflow-y-auto">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6 w-4/6 mx-auto">
          {users && users.map((user) => <UserCard key={user.id} user={user} />)}
        </div>
      </div>
    </PageLayout>
  );
}

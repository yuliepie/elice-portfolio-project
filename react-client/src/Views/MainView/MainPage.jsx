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
      <div className="bg-yellow-200 w-full h-32 flex gap-4 items-center justify-center">
        <input
          name="searchbox"
          type="text"
          className="form-style w-3/4"
          placeholder="프로필을 검색해보세요!"
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={fetchQueriedUsers}
          className="bg-indigo-300 p-2 rounded-md w-20"
        >
          검색
        </button>
      </div>
      <div className="px-20 py-6">
        <div className="flex flex-wrap gap-6 border-2 border-blue-500">
          {users && users.map((user) => <UserCard key={user.id} user={user} />)}
        </div>
      </div>
    </PageLayout>
  );
}

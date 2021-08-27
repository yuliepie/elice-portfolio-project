import PageLayout from "../../Components/PageLayout";
import axios from "axios";
import { useEffect, useState } from "react";
import UserCard from "./UserCard";
import { animateScroll as scroll } from "react-scroll";

export default function MainPage() {
  const [users, setUsers] = useState(null);
  const [query, setQuery] = useState("");
  const [validQuery, setValidQuery] = useState(true);

  // API Fetch
  async function fetchAllUsers() {
    try {
      const response = await axios.get("/api/users");
      setUsers(response.data.users);
      return response.data.users.length;
    } catch (err) {
      console.error(err);
    }
  }
  useEffect(() => {
    fetchAllUsers();
  }, []);

  async function fetchQueriedUsers() {
    try {
      const response = await axios.get(`/api/users?name=${query}`);
      setUsers(response.data.users);
      return response.data.users.length;
    } catch (err) {
      console.error(err);
    }
  }

  function fetchUsers() {
    if (query.length === 0) {
      setValidQuery(true);
      fetchAllUsers().then((length) => {
        if (length) {
          scrollToResults();
        }
      });
    } else if (query.length < 2) {
      setValidQuery(false);
      return;
    } else {
      setValidQuery(true);
      fetchQueriedUsers().then((length) => {
        if (length) {
          scrollToResults();
        }
      });
    }
  }

  const scrollToResults = () => {
    scroll.scrollTo(310, {
      duration: 400,
      smooth: true,
    });
  };

  const scrollToTop = () => {
    scroll.scrollToTop({
      duration: 500,
      smooth: true,
    });
  };

  return (
    <PageLayout>
      <div className="bg-indigo-500 bg-opacity-80 w-full h-80 flex flex-col items-center justify-center">
        <div className="header-text">Find your next connection.</div>
        <div className="mt-8 w-1/3 pl-6 py-1 pr-1 rounded-full bg-white inline-flex justify-end shadow-lg">
          <input
            name="searchbox"
            type="text"
            className="focus:ring-transparent p-2 text-sm transparent border-none flex-1"
            placeholder="프로필을 검색해보세요!"
            autoComplete="off"
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            onClick={fetchUsers}
            className="main-btn w-20 bg-red-400 hover:bg-opacity-80"
          >
            검색
          </button>
        </div>
        <p
          className={`mt-1 text-sm text-transparent shared-transition ${
            !validQuery && "text-white"
          }`}
        >
          두글자 이상 입력해주세요!
        </p>
      </div>
      <div
        className="px-20 py-10 overflow-y-auto min-h-screen"
        id="resultsContainer"
        name="resultsContainer"
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6 w-4/6 mx-auto">
          {users && users.map((user) => <UserCard key={user.id} user={user} />)}
        </div>
        {users && !users.length && (
          <div className="text-center text-gray-500 p-8">
            <div className="">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-20 w-20 mx-auto"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <h3 className="text-3xl mt-4">검색결과 없음</h3>
            <p className="mt-4">다른 키워드를 검색해보세요.</p>
          </div>
        )}
      </div>
      <button
        onClick={scrollToTop}
        className="fixed bottom-10 right-10 p-2 bg-white border border-gray-300 shadow-md"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-5 w-5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M4.293 15.707a1 1 0 010-1.414l5-5a1 1 0 011.414 0l5 5a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414 0zm0-6a1 1 0 010-1.414l5-5a1 1 0 011.414 0l5 5a1 1 0 01-1.414 1.414L10 5.414 5.707 9.707a1 1 0 01-1.414 0z"
            clipRule="evenodd"
          />
        </svg>
      </button>
    </PageLayout>
  );
}

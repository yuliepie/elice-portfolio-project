import { Link } from "react-router-dom";

export default function LoginForm() {
  return (
    <div>
      <div>
        <form className="my-4">
          <div className="grid grid-cols-1 gap-6">
            <label className="block">
              <span className="text-gray-700">아이디 (이메일):</span>
              <input
                type="email"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                placeholder="john@example.com"
              />
            </label>
            <label className="block">
              <span className="text-gray-700">비밀번호:</span>
              <input
                type="password"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              />
            </label>
            <button type="submit" className="bg-blue-200 w-20 p-2 mx-auto">
              로그인
            </button>
          </div>
        </form>
        <div className="text-center">
          <Link to="/signup" className="w-max-content">
            <span className="border-b-2 border-blue-500 w-max-content text-blue-500">
              아직 회원이 아니신가요?
            </span>
          </Link>
        </div>
      </div>
    </div>
  );
}

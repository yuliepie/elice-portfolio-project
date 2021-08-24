import PageLayout from "../../Components/PageLayout";
import SignUpForm from "./SignUpForm";

export default function SignUpPage() {
  return (
    <PageLayout>
      <div className="bg-indigo-500 bg-opacity-80 flex flex-col py-16 justify-start items-center h-full">
        <h2 className="header-text font-extrabold">회원가입.</h2>
        <div className="w-1/2 mt-8 p-8 bg-white rounded-xl shadow-md">
          <SignUpForm />
        </div>
      </div>
    </PageLayout>
  );
}

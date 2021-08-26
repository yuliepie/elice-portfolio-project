export default function DeleteButton({ handleDelete }) {
  return (
    <div
      className="bg-transparent text-red-500 cursor-pointer absolute top-5 right-5 hover:text-opacity-80"
      onClick={handleDelete}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-8 w-8"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fillRule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 000 2h6a1 1 0 100-2H7z"
          clipRule="evenodd"
        />
      </svg>
    </div>
  );
}

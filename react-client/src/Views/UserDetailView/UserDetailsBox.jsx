export default function UserDetailsBox({
  children,
  title,
  pageInEditMode,
  isEditing,
  setIsEditing,
  setBoxesInEdit,
  handleAdd,
  validate,
}) {
  return (
    <div className="w-full py-4 mb-6 relative">
      <h2 className="ml-2 pb-3 pl-2 font-bold text-3xl border-b-4 border-dotted border-red-300">
        {title}
      </h2>
      <div className="mt-4 ml-8 flex flex-col divide-y divide-gray-400 divide-opacity-80 divide-dotted gap-2">
        {children}
      </div>
      {pageInEditMode && !isEditing && (
        <button
          onClick={() => {
            setIsEditing(true);
            setBoxesInEdit((prev) => prev + 1);
          }}
          className="edit-btn absolute top-4 right-2"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
            <path
              fillRule="evenodd"
              d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"
              clipRule="evenodd"
            />
          </svg>
        </button>
      )}
      {isEditing && (
        <>
          {/* 수정완료 버튼 */}
          <button
            onClick={() => {
              const isValid = validate();
              if (isValid) {
                setIsEditing(false);
                setBoxesInEdit((prev) => prev - 1);
              } else {
                alert("모든 항목을 입력하세요.");
              }
            }}
            className="edit-btn text-sm p-2 rounded-lg absolute top-4 right-2 text-white shadow-lg hover:bg-opacity-50 transition duration-200 ease-in-out"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
          </button>
          {/* 추가버튼 */}
          <button
            onClick={handleAdd}
            className="edit-btn ml-8 mt-4 bg-white border border-gray-400 border-opacity-80 text-gray-900 hover:bg-opacity-50 hover:bg-gray-200 transition duration-100 ease-in-out mx-auto"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-7 w-7 mx-auto"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </>
      )}
    </div>
  );
}

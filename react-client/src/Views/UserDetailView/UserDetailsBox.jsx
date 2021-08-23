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
    <div className="border-gray-500 border rounded-md px-8 pt-4 pb-10 relative">
      <h2 className="font-bold text-lg">{title}</h2>
      <div className="flex flex-col divide-y divide-red-500 gap-2">
        {children}
      </div>
      {pageInEditMode && !isEditing && (
        <button
          onClick={() => {
            setIsEditing(true);
            setBoxesInEdit((prev) => prev + 1);
          }}
          className="bg-red-200 text-sm p-2 rounded-lg absolute top-2 right-2"
        >
          수정
        </button>
      )}
      {isEditing && (
        <>
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
            className="bg-green-200 text-sm p-2 rounded-lg absolute top-2 right-2"
          >
            완료
          </button>
          <button
            onClick={handleAdd}
            className="bg-blue-200 text-sm p-2 rounded-lg absolute bottom-2 right-2"
          >
            추가
          </button>
        </>
      )}
    </div>
  );
}

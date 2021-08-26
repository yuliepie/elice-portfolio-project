import DeleteButton from "../Shared/DeleteButton";

export default function EducationForm({
  education,
  handleChange,
  handleDelete,
}) {
  return (
    <div className="pt-4 pb-4 relative">
      <input
        type="text"
        className="details-form-style"
        placeholder="학교이름"
        value={education.school_name}
        onChange={(e) =>
          handleChange(education.id, "school_name", e.target.value)
        }
      />
      <input
        type="text"
        className="details-form-style"
        required
        placeholder="전공"
        value={education.major}
        onChange={(e) => handleChange(education.id, "major", e.target.value)}
      />

      {/* Radio Buttons */}
      <div className="mt-4 flex gap-4">
        <label className="inline-flex items-center">
          <input
            className="form-radio"
            type="radio"
            name={"status_id" + education.id}
            value="1"
            checked={education.status_id == 1}
            onChange={(e) =>
              handleChange(education.id, "status_id", e.target.value)
            }
          />
          <span className="ml-2 text-gray-700 font-bold">재학중</span>
        </label>
        <label className="inline-flex items-center">
          <input
            className="form-radio"
            type="radio"
            name={"status_id" + education.id}
            value="2"
            checked={education.status_id == 2}
            onChange={(e) =>
              handleChange(education.id, "status_id", e.target.value)
            }
          />
          <span className="ml-2 text-gray-700 font-bold">학사졸업</span>
        </label>
        <label className="inline-flex items-center">
          <input
            className="form-radio"
            type="radio"
            name={"status_id" + education.id}
            value="3"
            checked={education.status_id == 3}
            onChange={(e) =>
              handleChange(education.id, "status_id", e.target.value)
            }
          />
          <span className="ml-2 text-gray-700 font-bold">석사졸업</span>
        </label>
        <label className="inline-flex items-center">
          <input
            className="form-radio"
            type="radio"
            name={"status_id" + education.id}
            value={4}
            checked={education.status_id == 4}
            onChange={(e) =>
              handleChange(education.id, "status_id", e.target.value)
            }
          />
          <span className="ml-2 text-gray-700 font-bold">박사졸업</span>
        </label>
      </div>
      {/* Delete Button */}
      <DeleteButton handleDelete={handleDelete} />
    </div>
  );
}

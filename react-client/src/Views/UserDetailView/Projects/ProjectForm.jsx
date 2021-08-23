export default function ProjectForm({ project, handleChange }) {
  return (
    <div className="py-4">
      <input
        type="text"
        className="details-form-style w-1/2"
        placeholder="프로젝트명"
        value={project.name}
        onChange={(e) => handleChange(project.id, "name", e.target.value)}
      />
      <input
        type="text"
        className="details-form-style w-full"
        placeholder="프로젝트 내용을 기록해주세요."
        value={project.description}
        onChange={(e) =>
          handleChange(project.id, "description", e.target.value)
        }
      />
      <div className="mt-2 flex gap-4">
        <label>
          <span className="text-gray-700 text-sm">시작: </span>
          <input
            className="text-sm"
            onChange={(e) =>
              handleChange(project.id, "start_date", e.target.value)
            }
            value={project.start_date}
            type="date"
          />
        </label>
        <label>
          <span className="text-gray-700 text-sm">종료: </span>
          <input
            className="text-sm"
            onChange={(e) =>
              handleChange(project.id, "end_date", e.target.value)
            }
            value={project.end_date}
            type="date"
          />
        </label>
      </div>
    </div>
  );
}
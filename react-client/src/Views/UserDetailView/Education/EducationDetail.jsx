import EducationStatus from "./EducationStatus";

export default function EducationDetail({ education }) {
  return (
    <div className="pt-2">
      <div>{education.school_name}</div>
      <div>
        {education.major} ({EducationStatus[education.status_id]})
      </div>
    </div>
  );
}

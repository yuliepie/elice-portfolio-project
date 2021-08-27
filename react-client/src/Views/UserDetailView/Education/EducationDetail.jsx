import EducationStatus from "./EducationStatus";

export default function EducationDetail({ education }) {
  return (
    <div className="user-detail-wrapper">
      <h3 className="user-detail-title">
        {education.school_name}
        <span className="float-right font-light text-sm">
          {EducationStatus[education.status_id]}
        </span>
      </h3>
      <p className="user-detail-desc">{education.major}</p>
    </div>
  );
}

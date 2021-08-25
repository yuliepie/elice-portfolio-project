import parseDate from "../../../Helpers/DateParser";

export default function ProjectDetail({ project }) {
  const startDate = parseDate(project.start_date);
  const endDate = parseDate(project.end_date);

  return (
    <div className="user-detail-wrapper">
      <h3 className="user-detail-title">{project.name}</h3>
      <p className="user-detail-desc mt-2">{project.description}</p>
      <p className="user-detail-date pt-0">{`${startDate.year}년 ${startDate.month}월 - ${endDate.year}년 ${endDate.month}월`}</p>
    </div>
  );
}

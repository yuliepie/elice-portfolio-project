export default function ProjectDetail({ project }) {
  return (
    <div className="pt-2">
      <div className="font-bold">{project.name}</div>
      <div>{project.description}</div>
      <div>{`${project.start_date} - ${project.end_date}`}</div>
    </div>
  );
}

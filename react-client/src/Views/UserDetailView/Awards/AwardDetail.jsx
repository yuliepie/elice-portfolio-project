export default function AwardDetail({ award }) {
  return (
    <div className="pt-2">
      <div className="font-bold">{award.name}</div>
      <div>{award.description}</div>
    </div>
  );
}

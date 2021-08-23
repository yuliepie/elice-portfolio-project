export default function CertDetail({ cert }) {
  return (
    <div className="pt-2">
      <div className="font-bold">{cert.name}</div>
      <div>{cert.provider}</div>
      <div>{`${cert.acquired_date} 취득`}</div>
    </div>
  );
}

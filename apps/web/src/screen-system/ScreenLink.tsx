import { useEffect } from "react";
import { Link, useNavigate, type LinkProps } from "react-router-dom";
export function ScreenLink({ auto, ...props }: LinkProps & { auto?: boolean }) {
  const navigate = useNavigate();
  useEffect(() => { if (auto) navigate(props.to, { replace: false }); }, [auto, navigate, props.to]);
  return <Link {...props} />;
}

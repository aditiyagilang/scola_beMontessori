import * as React from "react"
import Svg, { G, Path } from "react-native-svg"

function SvgComponent(props) {
  return (
    <Svg className='h-10 w-20'
      viewBox="0 0 11 20"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <G
        transform="translate(-345 -3434) translate(100 3378) translate(238 54)"
        stroke="none"
        strokeWidth={1}
        fill="none"
        fillRule="evenodd"
      >
        <Path opacity={0.87} d="M24 24L0 24 0 0 24 0z" />
        <Path
          d="M7.38 21.01c.49.49 1.28.49 1.77 0l8.31-8.31a.996.996 0 000-1.41L9.15 2.98a1.25 1.25 0 00-1.77 0 1.25 1.25 0 000 1.77L14.62 12l-7.25 7.25c-.48.48-.48 1.28.01 1.76z"
          fill="#1D1D1D"
        />
      </G>
    </Svg>
  )
}

export default SvgComponent

import { Box, HStack, NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper, Text } from '@chakra-ui/react';

interface EmotionCfg {
  exaggeration: number;
  cfg: number;
  temperature: number;
  speed: number;
}

interface Props {
  value: EmotionCfg;
  onChange: (v: EmotionCfg) => void;
}

const clamp = (v: number) => Math.min(2, Math.max(0, v));

const EmotionTable = ({ value, onChange }: Props) => {
  const handleChange = (key: keyof EmotionCfg, val: string) => {
    const num = clamp(parseFloat(val));
    onChange({ ...value, [key]: isNaN(num) ? 1.0 : num });
  };

  return (
    <Box>
      {(Object.keys(value) as (keyof EmotionCfg)[]).map((key) => (
        <HStack key={key} mb={2}>
          <Text w="120px" textTransform="capitalize">
            {key}
          </Text>
          <NumberInput
            value={value[key]}
            step={0.05}
            min={0}
            max={2}
            precision={2}
            onChange={(_, v) => handleChange(key, String(v))}
            width="120px"
          >
            <NumberInputField />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
        </HStack>
      ))}
    </Box>
  );
};

export default EmotionTable; 
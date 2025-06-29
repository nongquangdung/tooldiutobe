import { Box, Heading, VStack } from '@chakra-ui/react';
import VoiceStudio from './components/VoiceStudio';

const App = () => {
  return (
    <Box p={4} maxW="1200px" mx="auto">
      <VStack spacing={6} align="stretch">
        <Heading size="lg">Voice Studio Web</Heading>
        <VoiceStudio />
      </VStack>
    </Box>
  );
};

export default App; 